import calendar
import datetime
import locale
import re

import click


def _parse_month_name(month_name: str) -> int:
    """Parse a month name (full or abbreviated) to month number.

    Parameters
    ----------
    month_name: str
        Month name or abbreviation

    Returns
    -------
    int
        Month number (1-12)

    Raises
    ------
    ValueError
        If month name is invalid
    """
    month_name = month_name.capitalize()
    try:
        return list(calendar.month_name).index(month_name)
    except ValueError:
        try:
            return list(calendar.month_abbr).index(month_name)
        except ValueError:
            raise ValueError(f"Invalid month name: {month_name}")


def period_to_dates(period_str: str) -> list[str]:
    """Convert a period string to start and end dates in YYYY/MM/DD format.

    Supports various formats:
    - "last month", "this month"
    - "Jan 2024 to Mar 2024" (month ranges)
    - "January 2024" (single month)
    - "2024/01/15 to 2024/03/31" (explicit date ranges)

    Parameters
    ----------
    period_str: str
        Period description

    Returns
    -------
    list[str]
        [begin_date, end_date] in YYYY/MM/DD format
    """
    period_str = period_str.strip()
    now = datetime.datetime.now()

    # Handle "last month"
    if period_str.lower() == "last month":
        if now.month == 1:
            year = now.year - 1
            month = 12
        else:
            year = now.year
            month = now.month - 1
        begin_date = f"{year}/{month}/1"
        if month == 12:
            end_date = f"{year+1}/1/1"
        else:
            end_date = f"{year}/{month+1}/1"
        return [begin_date, end_date]

    # Handle "this month"
    if period_str.lower() == "this month":
        begin_date = f"{now.year}/{now.month}/1"
        if now.month == 12:
            end_date = f"{now.year+1}/1/1"
        else:
            end_date = f"{now.year}/{now.month+1}/1"
        return [begin_date, end_date]

    # Handle "Month to Month" format (defaults to current year)
    month_range_no_year_pattern = r"^(\w+)\s+to\s+(\w+)$"
    match = re.match(month_range_no_year_pattern, period_str, re.IGNORECASE)
    if match:
        start_month_name, end_month_name = match.groups()
        try:
            start_month = _parse_month_name(start_month_name)
            end_month = _parse_month_name(end_month_name)
        except ValueError as e:
            raise click.UsageError(f"Invalid month name in period: {period_str}")

        # Use current year for END date (people typically look backwards)
        end_year = now.year

        # If end month is before start month, it's a year rollover (e.g., "Dec to Jan")
        # Start date should be in the previous year
        if end_month < start_month:
            start_year = end_year - 1
        else:
            start_year = end_year

        begin_date = f"{start_year}/{start_month}/1"

        # End date is first day of month after end_month
        if end_month == 12:
            end_date = f"{end_year+1}/1/1"
        else:
            end_date = f"{end_year}/{end_month+1}/1"
        return [begin_date, end_date]

    # Handle "Month YYYY to Month YYYY" format
    month_range_pattern = r"^(\w+)\s+(\d{4})\s+to\s+(\w+)\s+(\d{4})$"
    match = re.match(month_range_pattern, period_str, re.IGNORECASE)
    if match:
        start_month_name, start_year_str, end_month_name, end_year_str = match.groups()
        start_year = int(start_year_str)
        end_year = int(end_year_str)
        try:
            start_month = _parse_month_name(start_month_name)
            end_month = _parse_month_name(end_month_name)
        except ValueError:
            raise click.UsageError(f"Invalid month name in period: {period_str}")

        begin_date = f"{start_year}/{start_month}/1"
        # End date is first day of month after end_month
        if end_month == 12:
            end_date = f"{end_year+1}/1/1"
        else:
            end_date = f"{end_year}/{end_month+1}/1"
        return [begin_date, end_date]

    # Handle "Month YYYY" format (single month)
    single_month_pattern = r"^(\w+)\s+(\d{4})$"
    match = re.match(single_month_pattern, period_str, re.IGNORECASE)
    if match:
        month_name, year_str = match.groups()
        year = int(year_str)
        try:
            month = _parse_month_name(month_name)
        except ValueError:
            raise click.UsageError(f"Invalid month name: {month_name}")

        begin_date = f"{year}/{month}/1"
        if month == 12:
            end_date = f"{year+1}/1/1"
        else:
            end_date = f"{year}/{month+1}/1"
        return [begin_date, end_date]

    # Handle explicit date range "YYYY/MM/DD to YYYY/MM/DD"
    date_range_pattern = r"^(\d{4}/\d{1,2}/\d{1,2})\s+to\s+(\d{4}/\d{1,2}/\d{1,2})$"
    match = re.match(date_range_pattern, period_str)
    if match:
        begin_date, end_date = match.groups()
        return [begin_date, end_date]

    raise click.UsageError(
        f"Invalid period format: '{period_str}'. "
        "Supported formats: 'last month', 'this month', 'Jan to Mar', "
        "'Jan 2024 to Mar 2024', 'January 2024', or 'YYYY/MM/DD to YYYY/MM/DD'"
    )


def month_to_dates(month_str: str) -> list[str]:
    """Convert month to a start and end dates in YYYY/MM/DD format.

    Parameters
    ----------
    month_str: str
        Name of Month

    Returns
    -------
        list[begin_date, end_date]
    """
    year = datetime.datetime.now().year
    try:
        month_num = list(calendar.month_name).index(month_str)
    except ValueError:
        raise click.UsageError(f"{month_str} is not a valid month name.")

    begin_date = f"{year}/{month_num}/1"

    # Ledger goes up to, but not including the end date.
    if month_num == 12:
        end_date = f"{year+1}/1/1"
    else:
        end_date = f"{year}/{month_num+1}/1"

    return [begin_date, end_date]


def reverse_sign(accounts: dict) -> dict:
    """Reverse the sign of the account balance and format it.

    Parameters
    ----------
    accouts: dict
        [account:  bal]

    Returns
    -------
    Dict
        [Account Name: bal]

    """
    for acc in accounts.copy():
        accounts[acc] = format_negative_numbers(accounts[acc] * -1)
    return accounts


def format_negative_numbers(number) -> str:
    """Return the absolute value of a number and wrap in parentheses if negative.

    Paramaters
    ----------
    number: int
        Number to be formatted

    Returns
    -------
    Str
        Number as a string, if negative enclosed in parentheses.
    """
    if number < 0:
        return "(" + format_balance(abs(number)) + ")"

    return number


def format_balance(int_balance):
    """Format balance.

    Formats balance using the locale seperators for numbers.  Removes
    negative signs and instead encloses negative balances in parentheses.

    Parameters
    ----------
    int_balance: (dict, int)


    Returns
    -------
    (dict, int)
       Balance formatted with locale seperator.
    """
    locale.setlocale(locale.LC_ALL, "")

    if isinstance(int_balance, int):
        balance = format_negative_numbers(int_balance)
        return f"{balance:n}"

    if isinstance(int_balance, dict):
        for account, balance in int_balance.items():
            if isinstance(balance, dict):
                format_balance(balance)
            elif isinstance(balance, int):
                balance = format_negative_numbers(balance)
                if isinstance(balance, str):
                    int_balance[account] = balance
                else:
                    int_balance[account] = f"{balance:n}"

    return int_balance
