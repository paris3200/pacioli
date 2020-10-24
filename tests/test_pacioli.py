import pytest
import subprocess
import locale

from pacioli import __version__
from pacioli.pacioli import Pacioli


def test_version():
    assert __version__ == "0.3.1"


def test_ledger_available():
    "Verify ledger is availabe on the system"
    output = subprocess.run(["ledger", "--version"], capture_output=True)
    assert output.returncode == 0


def test_get_balance_returns_int():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")

    checking = pacioli.get_balance("Assets:Current:Checking", date="2020/3/31")
    assert checking == 4138
    assert isinstance(checking, int)


def test_get_account_short_name_returns_account_name_from_full_account_listing():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    name = pacioli.get_account_short_name("Assets:Current:Checking")
    assert name == "checking"


def test_get_account_short_name_replaces_spaces_with_underscores():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    name = pacioli.get_account_short_name("Assets:Longterm:Real Estate")
    assert name == "real_estate"


def test_format_balance_dict_input_returns_formatted_dict():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    locale.setlocale(locale.LC_ALL, "")
    checking = f"{11000:n}"
    savings = f"{25000:n}"
    test_numbers = {"Checking": 11000, "Savings": 25000}
    result = pacioli.format_balance(test_numbers)

    assert {"Checking": checking, "Savings": savings} == result


def test_format_balance_int_input_returns_formmated_str():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    locale.setlocale(locale.LC_ALL, "")
    checking = f"{11000:n}"
    result = pacioli.format_balance(11000)
    assert checking == result


def test_format_negative_numbers_returns_negative_number_in_parentheses():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    n = int(-100)
    result = pacioli.format_negative_numbers(n)
    assert "(100)" == result


def test_format_net_gain_returns_negative_number_in_parentheses_with_locale_formatting():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    locale.setlocale(locale.LC_ALL, "")
    n = int(-1000)
    n_positive = n * -1
    result = pacioli.format_negative_numbers(n)
    assert f"({n_positive:n})" == result


def test_run_system_command_raises_error_on_invalid_command():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    with pytest.raises(Exception):
        pacioli.run_system_command(["foobar"])


def test_render_template_raises_error_on_template_not_found():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")
    with pytest.raises(FileNotFoundError):
        pacioli.render_template("foo.tex", {"Checking": 100})
