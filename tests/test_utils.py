import datetime

import pytest
from pacioli.utils import month_timeframe


def test_month_timeframe() -> None:
    year = datetime.datetime.now().year

    expected = [f"{year}/3/1", f"{year}/4/1"]
    assert month_timeframe("March") == expected


def test_month_timeframe_december() -> None:
    year = datetime.datetime.now().year

    expected = [f"{year}/12/1", f"{year+1}/1/1"]
    assert month_timeframe("December") == expected


@pytest.mark.skip("Not implemented.")
def test_month_timeframe_invalid_month() -> None:
    expected = ""
    assert month_timeframe("foo") == expected
