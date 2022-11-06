"""Tests Utils."""
import datetime

import pytest
from pacioli.utils import month_to_dates


def test_month_to_dates() -> None:
    """Test month is converted correctly."""
    year = datetime.datetime.now().year

    expected = [f"{year}/3/1", f"{year}/4/1"]
    assert month_to_dates("March") == expected


def test_month_to_dates_december() -> None:
    """Test decemeber rolls over to the new year."""
    year = datetime.datetime.now().year

    expected = [f"{year}/12/1", f"{year+1}/1/1"]
    assert month_to_dates("December") == expected


def test_month_to_dates_invalid_month() -> None:
    """Raises an exception on invalid month."""
    with pytest.raises(Exception):
        month_to_dates("foo")


@pytest.mark.skip("Not implemented")
def test_month_to_dates_uses_date_format() -> None:
    """Test use of date format from config file."""
    assert False
