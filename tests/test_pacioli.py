import subprocess

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

    checking = pacioli.get_balance("Assets:Current:Checking")
    assert checking == 3648


def test_process_category():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    current_assets = pacioli.config.current_assets
    assert {
        "checking": 3648,
        "savings": 10030,
        "current_assets_total": 13678,
    } == pacioli.process_category(current_assets, "current_assets")


def test_account_name():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    name = pacioli.get_account_name("Assets:Current:Checking")
    assert name == "checking"


def test_account_name_with_spaces():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    name = pacioli.get_account_name("Assets:Longterm:Real Estate")
    assert name == "real_estate"


def test_balance_sheet():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")

    result = pacioli.balance_sheet()
    assert "Acme LLC" in result
    assert "& Checking  & 3648 \\" in result
    assert "& Savings  & 10030 \\" in result
    assert "{Total Longterm Assets} & & 325576" in result
    assert "{Total Current Assets}} & & 13678\\" in result
    assert "{Total Secured Liabilities} & & 184654\\" in result


def test_compile_template():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")

    current_assets = pacioli.config.current_assets
    longterm_assets = pacioli.config.longterm_assets

    ledger = {}

    ledger.update(pacioli.process_category(current_assets, "current_assets"))
    ledger.update(pacioli.process_category(longterm_assets, "longterm_assets"))

    result = pacioli.compile_template(ledger)

    assert "& Checking  & 3648 \\" in result
    assert "& Savings  & 10030 \\" in result
    assert "{Total Current Assets}} & & 13678\\" in result
