"""Tests Utils."""

import datetime
import locale
from unittest.mock import patch

import pytest
from click.exceptions import UsageError

from pacioli.utils import (
    format_balance,
    format_negative_numbers,
    month_to_dates,
    period_to_dates,
)


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


def test_period_to_dates_last_month() -> None:
    """Test 'last month' period string."""
    now = datetime.datetime.now()
    if now.month == 1:
        expected_year = now.year - 1
        expected_month = 12
    else:
        expected_year = now.year
        expected_month = now.month - 1

    begin_date = f"{expected_year}/{expected_month}/1"
    if expected_month == 12:
        end_date = f"{expected_year+1}/1/1"
    else:
        end_date = f"{expected_year}/{expected_month+1}/1"

    result = period_to_dates("last month")
    assert result == [begin_date, end_date]


def test_period_to_dates_this_month() -> None:
    """Test 'this month' period string."""
    now = datetime.datetime.now()
    begin_date = f"{now.year}/{now.month}/1"
    if now.month == 12:
        end_date = f"{now.year+1}/1/1"
    else:
        end_date = f"{now.year}/{now.month+1}/1"

    result = period_to_dates("this month")
    assert result == [begin_date, end_date]


def test_period_to_dates_month_range() -> None:
    """Test month range format like 'Jan 2024 to Mar 2024'."""
    result = period_to_dates("Jan 2024 to Mar 2024")
    assert result == ["2024/1/1", "2024/4/1"]


def test_period_to_dates_month_range_full_names() -> None:
    """Test month range with full month names."""
    result = period_to_dates("January 2024 to March 2024")
    assert result == ["2024/1/1", "2024/4/1"]


def test_period_to_dates_month_range_december() -> None:
    """Test month range ending in December rolls over year."""
    result = period_to_dates("Oct 2024 to Dec 2024")
    assert result == ["2024/10/1", "2025/1/1"]


def test_period_to_dates_single_month() -> None:
    """Test single month format like 'January 2024'."""
    result = period_to_dates("January 2024")
    assert result == ["2024/1/1", "2024/2/1"]


def test_period_to_dates_single_month_abbreviated() -> None:
    """Test single month with abbreviated name."""
    result = period_to_dates("Jan 2024")
    assert result == ["2024/1/1", "2024/2/1"]


def test_period_to_dates_single_month_december() -> None:
    """Test single month December rolls over year."""
    result = period_to_dates("December 2024")
    assert result == ["2024/12/1", "2025/1/1"]


def test_period_to_dates_explicit_date_range() -> None:
    """Test explicit date range format."""
    result = period_to_dates("2024/1/15 to 2024/3/31")
    assert result == ["2024/1/15", "2024/3/31"]


def test_period_to_dates_invalid_format() -> None:
    """Test that invalid format raises UsageError."""
    with pytest.raises(UsageError):
        period_to_dates("invalid period")


def test_period_to_dates_invalid_month_name() -> None:
    """Test that invalid month name raises UsageError."""
    with pytest.raises(UsageError):
        period_to_dates("Foo 2024 to Bar 2024")


def test_period_to_dates_month_range_no_year() -> None:
    """Test 'Jan to Mar' format (same year, no rollover)."""
    now = datetime.datetime.now()
    result = period_to_dates("Jan to Mar")
    # Should use current year for both
    assert result == [f"{now.year}/1/1", f"{now.year}/4/1"]


def test_period_to_dates_month_range_no_year_rollover() -> None:
    """Test 'Dec to January' format (year rollover)."""
    now = datetime.datetime.now()
    result = period_to_dates("Dec to January")
    # Should use previous year for start, current year for end
    assert result == [f"{now.year-1}/12/1", f"{now.year}/2/1"]


def test_period_to_dates_month_range_no_year_rollover_full_names() -> None:
    """Test 'November to February' format (year rollover with full names)."""
    now = datetime.datetime.now()
    result = period_to_dates("November to February")
    # Should use previous year for start, current year for end
    assert result == [f"{now.year-1}/11/1", f"{now.year}/3/1"]


def test_period_to_dates_month_range_no_year_mixed() -> None:
    """Test mixed abbreviations and full names."""
    now = datetime.datetime.now()
    result = period_to_dates("Oct to March")
    # Year rollover: Oct is after March, so Oct is previous year
    assert result == [f"{now.year-1}/10/1", f"{now.year}/4/1"]


def test_period_to_dates_month_range_no_year_december() -> None:
    """Test month range ending in December without year (e.g., 'Jan to Dec')."""
    now = datetime.datetime.now()
    result = period_to_dates("Jan to Dec")
    assert result == [f"{now.year}/1/1", f"{now.year+1}/1/1"]


def test_period_to_dates_month_range_no_year_invalid_month() -> None:
    """Test invalid month name in month range without year raises UsageError."""
    with pytest.raises(UsageError):
        period_to_dates("Foo to Bar")


def test_period_to_dates_single_month_invalid_name() -> None:
    """Test invalid month name in single month format raises UsageError."""
    with pytest.raises(UsageError):
        period_to_dates("Foo 2024")


@patch("pacioli.utils.datetime")
def test_period_to_dates_last_month_january(mock_datetime) -> None:
    """Test 'last month' when current month is January."""
    mock_datetime.datetime.now.return_value = datetime.datetime(2024, 1, 15)
    result = period_to_dates("last month")
    assert result == ["2023/12/1", "2024/1/1"]


@patch("pacioli.utils.datetime")
def test_period_to_dates_last_month_non_january(mock_datetime) -> None:
    """Test 'last month' when current month is not January."""
    mock_datetime.datetime.now.return_value = datetime.datetime(2024, 5, 15)
    result = period_to_dates("last month")
    assert result == ["2024/4/1", "2024/5/1"]


@patch("pacioli.utils.datetime")
def test_period_to_dates_last_month_december_rollover(mock_datetime) -> None:
    """Test 'last month' when last month was December (current month is January)."""
    mock_datetime.datetime.now.return_value = datetime.datetime(2024, 2, 15)
    result = period_to_dates("last month")
    # Last month was January, so it should be Jan 1 to Feb 1
    assert result == ["2024/1/1", "2024/2/1"]


@patch("pacioli.utils.datetime")
def test_period_to_dates_this_month_december(mock_datetime) -> None:
    """Test 'this month' when current month is December."""
    mock_datetime.datetime.now.return_value = datetime.datetime(2024, 12, 15)
    result = period_to_dates("this month")
    assert result == ["2024/12/1", "2025/1/1"]


@patch("pacioli.utils.datetime")
def test_period_to_dates_this_month_non_december(mock_datetime) -> None:
    """Test 'this month' when current month is not December."""
    mock_datetime.datetime.now.return_value = datetime.datetime(2024, 5, 15)
    result = period_to_dates("this month")
    assert result == ["2024/5/1", "2024/6/1"]
