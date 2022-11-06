import calendar
import datetime

import click


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
