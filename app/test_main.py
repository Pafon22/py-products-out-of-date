import pytest
from app.main import outdated_products, datetime


products = [
    {
        "name": "salmon",
        "expiration_date": datetime.date(2022, 2, 10),
        "price": 600
    },
    {
        "name": "chicken",
        "expiration_date": datetime.date(2022, 2, 5),
        "price": 120
    },
    {
        "name": "duck",
        "expiration_date": datetime.date(2022, 2, 1),
        "price": 160
    }
]


@pytest.mark.parametrize(
    "year, month, day, result",
    [
        (2021, 1, 1, []),
        (2021, 1, 31, []),
        (2021, 12, 1, []),
        (2023, 1, 1, ["salmon", "chicken", "duck"]),
        (2023, 1, 31, ["salmon", "chicken", "duck"]),
        (2023, 12, 1, ["salmon", "chicken", "duck"]),
        (2022, 1, 1, []),
        (2022, 1, 31, []),
        (2022, 12, 1, ["salmon", "chicken", "duck"]),
        (2022, 2, 1, []),
        (2022, 2, 2, ["duck"]),
        (2022, 2, 6, ["chicken", "duck"]),
    ]
)
def test_outdated_products(
    monkeypatch: pytest.MonkeyPatch,
    year: int, month: int, day: int, result: list[str]
) -> None:
    # today is immutable and can't to be edited by setattr
    # so use heritage to the parent datetime.date
    # and substitute the method today there.
    class MockDate(datetime.date):
        @classmethod
        def today(cls) -> datetime.date:
            return datetime.date(year, month, day)

    monkeypatch.setattr("app.main.datetime.date", MockDate)
    assert outdated_products(products) == result
