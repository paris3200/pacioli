"""Tests for the blance sheet."""
import locale

import pytest
from pacioli.balance_sheet import BalanceSheet


def test_render_returns_report_formatted_as_tex():
    """It returns report formatted as tex."""
    report = BalanceSheet(config_file="tests/resources/sample_config.yml")
    locale.setlocale(locale.LC_ALL, "")
    checking = f"{int(4138):n}"
    savings = f"{int(10030):n}"
    total_liabilities = f"{int(186202):n}"
    assets = f"{int(339744):n}"

    result = report.print_report(date="2020/3/31")
    assert "Acme LLC" in result
    assert f"& Checking  & {checking} \\" in result
    assert f"& Savings  & {savings} \\" in result
    assert assets in result
    assert "Total Liabilities}" in result
    assert total_liabilities in result  # Value of Total Liabilities


def test_process_accounts_returns_dict_with_account_balances():
    """It returns account balances in a dict."""
    report = BalanceSheet(config_file="tests/resources/sample_config.yml")
    current_assets = report.config.current_assets
    result = report.process_accounts(current_assets, "current_assets", date="2020/3/31")
    assert {
        "checking": 4138,
        "savings": 10030,
        "current_assets_total": 14168,
    } == result
    assert isinstance(result, dict)


def test_render_template_returns_correct_data_in_template():
    """It returns correct data in template."""
    report = BalanceSheet(config_file="tests/resources/sample_config.yml")

    current_assets = report.config.current_assets
    longterm_assets = report.config.longterm_assets

    ledger = {}

    ledger.update(
        report.process_accounts(current_assets, "current_assets", date="2020/3/31")
    )
    ledger.update(
        report.process_accounts(longterm_assets, "longterm_assets", date="2020/3/31")
    )

    result = report.render_template(report.template, ledger)

    assert "Checking" in result
    assert "4138" in result  # Checking Balance
    assert "Savings" in result
    assert "10030" in result  # Savings Balance
    assert "Total Current Assets" in result
    assert "14168" in result  # Total Current Assets Balance


@pytest.mark.skip("Not Implemented")
def test_positive_liability_balance_is_displayed_as_negative():
    report = BalanceSheet(config_file="tests/resources/sample_config.yml")
    result = report.print_report(date="2020/3/31")

    assert "Prepay" in result
    assert "(100)" in result
