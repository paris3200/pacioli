"""Tests for cash flow statement."""

import locale

from pacioli.cash_flow_statement import CashFlowStatement
from pacioli.utils import format_balance


def test_get_total_cash_balance():
    """It returns the total of all cash accounts."""
    report = CashFlowStatement(config_file="tests/resources/sample_config.yml")
    # Balance at end of March 31: should reflect all transactions through that date
    # Using --end 2020/04/01 includes transactions through 2020/03/31
    result = report.get_total_cash_balance("2020/04/01")
    assert result == 14168


def test_process_accounts_calculates_net_change():
    """It returns net change in account balances over period."""
    report = CashFlowStatement(config_file="tests/resources/sample_config.yml")

    # Test with operating activities
    operating = report.process_accounts(
        report.config.operating_activities, start_date="2020/02/01", end_date="2020/03/31"
    )

    # Should have accounts and category total
    assert "category_total" in operating
    assert isinstance(operating["category_total"], int)


def test_print_report_returns_formatted_tex():
    """It returns report formatted as tex."""
    report = CashFlowStatement(config_file="tests/resources/sample_config.yml")
    start_date = "2020/02/01"
    end_date = "2020/03/31"

    result = report.print_report(start_date, end_date)

    assert "Acme LLC" in result
    assert "Cash Flow Statement" in result
    assert "OPERATING ACTIVITIES" in result
    assert "INVESTING ACTIVITIES" in result
    assert "FINANCING ACTIVITIES" in result
    assert "Net Cash from Operating Activities" in result
    assert "Net Change in Cash" in result
    assert "Beginning Cash Balance" in result
    assert "ENDING CASH BALANCE" in result


def test_reconciliation_balances():
    """Beginning cash + net change = ending cash."""
    report = CashFlowStatement(config_file="tests/resources/sample_config.yml")
    # Period from Feb 2 through March 31 (after opening balances on Feb 1)
    # Beginning balance: --end 2020/02/02 = end of Feb 1 (includes opening)
    # Period activities: -b 2020/02/02 -e 2020/04/01
    # Ending balance: --end 2020/04/01 = end of March 31
    start_date = "2020/02/02"
    end_date = "2020/04/01"

    # For cash balances, use --end which means "before this date"
    beginning = report.get_total_cash_balance(start_date)  # --end 2020/02/02 = after Feb 1
    ending = report.get_total_cash_balance(end_date)  # --end 2020/04/01 = after Mar 31

    # Process all activities
    operating = report.process_accounts(report.config.operating_activities, start_date, end_date)
    investing = report.process_accounts(report.config.investing_activities, start_date, end_date)
    financing = report.process_accounts(report.config.financing_activities, start_date, end_date)

    net_change = (
        operating["category_total"] + investing["category_total"] + financing["category_total"]
    )

    # Verify reconciliation (allow ±1 for rounding differences)
    assert abs((beginning + net_change) - ending) <= 1


def test_operating_activities_contains_expected_accounts():
    """It processes operating activity accounts correctly."""
    report = CashFlowStatement(config_file="tests/resources/sample_config.yml")
    start_date = "2020/02/01"
    end_date = "2020/04/01"

    operating = report.process_accounts(report.config.operating_activities, start_date, end_date)

    # Should have category total
    assert "category_total" in operating
    # Should have some activity (non-zero total)
    assert operating["category_total"] != 0


def test_render_template_returns():
    """It returns a rendered template."""
    report = CashFlowStatement(config_file="tests/resources/sample_config.yml")
    start_date = "2020/02/01"
    end_date = "2020/03/01"

    accounts = {
        "title": report.title,
        "start_date": start_date,
        "end_date": end_date,
    }

    # Calculate cash balances
    beginning_cash = report.get_total_cash_balance(start_date)
    ending_cash = report.get_total_cash_balance(end_date)

    # Process each section
    operating = report.process_accounts(report.config.operating_activities, start_date, end_date)
    accounts["operating_activities_total"] = operating.pop("category_total")
    accounts["operating_activities"] = operating

    investing = report.process_accounts(report.config.investing_activities, start_date, end_date)
    accounts["investing_activities_total"] = investing.pop("category_total")
    accounts["investing_activities"] = investing

    financing = report.process_accounts(report.config.financing_activities, start_date, end_date)
    accounts["financing_activities_total"] = financing.pop("category_total")
    accounts["financing_activities"] = financing

    accounts["net_change_in_cash"] = (
        accounts["operating_activities_total"]
        + accounts["investing_activities_total"]
        + accounts["financing_activities_total"]
    )
    accounts["beginning_cash"] = beginning_cash
    accounts["ending_cash"] = ending_cash

    result = report.render_template(report.template, format_balance(accounts))

    locale.setlocale(locale.LC_ALL, "")

    # Verify basic content
    assert "Acme LLC" in result
    assert "OPERATING ACTIVITIES" in result
    assert "INVESTING ACTIVITIES" in result
    assert "FINANCING ACTIVITIES" in result
