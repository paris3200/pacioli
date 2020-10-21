import subprocess
import locale

from pacioli import __version__
from pacioli.pacioli import Pacioli


def test_version():
    assert __version__ == "0.1.0"


def test_ledger_available():
    "Verify ledger is availabe on the system"
    output = subprocess.run(["ledger", "--version"], capture_output=True)
    assert output.returncode == 0


def test_get_balance_returns_int():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")

    checking = pacioli.get_balance("Assets:Current:Checking", date="2020/3/31")
    assert checking == 4138


def test_process_account_list():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    current_assets = pacioli.config.current_assets
    assert {
        "checking": 4138,
        "savings": 10030,
        "current_assets_total": 14168,
    } == pacioli.process_account_list(
        current_assets, "current_assets", date="2020/3/31"
    )


def test_process_account():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    assert {
        "Salary": 4913,
        "Interest": 40,
        "income_total": 4953,
    } == pacioli.process_account("Income", start_date="2020/2/1", end_date="2020/3/31")


def test_account_name():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    name = pacioli.get_account_short_name("Assets:Current:Checking")
    assert name == "checking"


def test_account_name_with_spaces():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    name = pacioli.get_account_short_name("Assets:Longterm:Real Estate")
    assert name == "real_estate"


def test_balance_sheet():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")

    locale.setlocale(locale.LC_ALL, "")
    checking = f"{int(4138):n}"
    savings = f"{int(10030):n}"
    total_liabilities = f"{int(186102):n}"
    assets = f"{int(339744):n}"

    result = pacioli.balance_sheet(date="2020/3/31")
    assert "Acme LLC" in result
    assert f"& Checking  & {checking} \\" in result
    assert f"& Savings  & {savings} \\" in result
    assert assets in result
    assert "Total Liabilities}" in result
    assert total_liabilities in result  # Value of Total Liabilities


def test_income_statement():

    locale.setlocale(locale.LC_ALL, "")
    income = f"{int(4953):n}"

    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    result = pacioli.income_statement(start_date="2020/2/1", end_date="2020/2/28")

    assert "Income Statement" in result
    assert "{Total Income}} & & %s \\" % income in result


def test_formatter_dict_input():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    locale.setlocale(locale.LC_ALL, "")
    checking = f"{11000:n}"
    savings = f"{25000:n}"
    test_numbers = {"Checking": 11000, "Savings": 25000}
    result = pacioli.format_balance(test_numbers)

    assert {"Checking": checking, "Savings": savings} == result


def test_formatter_int_input():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    locale.setlocale(locale.LC_ALL, "")
    checking = f"{11000:n}"
    result = pacioli.format_balance(11000)
    assert checking == result


def test_compile_template():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")

    current_assets = pacioli.config.current_assets
    longterm_assets = pacioli.config.longterm_assets

    ledger = {}

    ledger.update(
        pacioli.process_account_list(current_assets, "current_assets", date="2020/3/31")
    )
    ledger.update(
        pacioli.process_account_list(
            longterm_assets, "longterm_assets", date="2020/3/31"
        )
    )

    result = pacioli.compile_template("balance", ledger)

    assert "& Checking  & 4138 \\" in result
    assert "& Savings  & 10030 \\" in result
    assert "{Total Current Assets}} & & 14168\\" in result
