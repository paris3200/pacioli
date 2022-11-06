import datetime

import pytest
from pacioli.utils import format_negative_numbers
from pacioli.utils import month_to_dates


def test_month_to_dates() -> None:
    year = datetime.datetime.now().year

    expected = [f"{year}/3/1", f"{year}/4/1"]
    assert month_to_dates("March") == expected


def test_month_to_dates_december() -> None:
    year = datetime.datetime.now().year

    expected = [f"{year}/12/1", f"{year+1}/1/1"]
    assert month_to_dates("December") == expected


def test_month_to_dates_invalid_month() -> None:
    with pytest.raises(Exception):
        month_to_dates("foo")


def test_format_negative_numbers_returns_negative_number_in_parentheses():
    """It returns negative numbers in parentheses."""
    n = int(-100)
    result = format_negative_numbers(n)
    assert "(100)" == result


@pytest.mark.skip("Not implemented")
def test_month_to_dates_uses_date_format() -> None:
    assert False
