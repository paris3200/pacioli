"""Tests Utils."""
import datetime
import locale

import pytest
from pacioli.utils import format_balance
from pacioli.utils import format_negative_numbers
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


def test_format_net_gain_returns_negative_number_in_parentheses_with_locale_formatting():
    """It formats negative number with locacle formatting."""
    locale.setlocale(locale.LC_ALL, "")
    n = int(-1000)
    n_positive = n * -1
    result = format_negative_numbers(n)
    assert f"({n_positive:n})" == result


def test_format_balance_int_input_returns_formmated_str():
    """It returns a formatted str."""
    locale.setlocale(locale.LC_ALL, "")
    checking = f"{11000:n}"
    result = format_balance(11000)
    assert checking == result


def test_format_balance_dict_input_returns_formatted_dict():
    """It returns a formatted dictionary."""
    locale.setlocale(locale.LC_ALL, "")
    checking = f"{11000:n}"
    savings = f"{25000:n}"
    test_numbers = {"Checking": 11000, "Savings": 25000}
    result = format_balance(test_numbers)

    assert {"Checking": checking, "Savings": savings} == result


def test_format_negative_numbers_returns_negative_number_in_parentheses():
    """It returns negative numbers in parentheses."""
    n = int(-100)
    result = format_negative_numbers(n)
    assert "(100)" == result


@pytest.mark.skip("Not implemented")
def test_month_to_dates_uses_date_format() -> None:
    """Test use of date format from config file."""
    assert False
