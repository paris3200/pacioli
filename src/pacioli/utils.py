import calendar
import datetime
import locale

import click


def month_to_dates(month_str: str) -> list[str, str]:
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
