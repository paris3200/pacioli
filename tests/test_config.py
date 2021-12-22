"""Test the Config Class."""
import pytest

from pacioli.config import Config


def test_profile_set():
    """It checks that sample config settings are loaded."""
    config = Config("tests/resources/sample_config.yml")
    assert config.effective == "--effective"
    assert config.cleared == "--cleared"
    assert config.journal_file == "tests/resources/sample_ledger.ldg"
    assert config.balance_sheet_template == "test_balance_sheet.tex"
    assert config.income_sheet_template == "test_income_sheet.tex"
    assert config.DEBUG is True


def test_profile_set_with_pending_transactions():
    """It checks that sample config settings are loaded."""
    config = Config("tests/resources/sample_config_pending.yml")
    assert config.effective == "--effective"
    assert config.cleared is None
    assert config.journal_file == "tests/resources/sample_ledger.ldg"
    assert config.balance_sheet_template == "test_balance_sheet.tex"
    assert config.income_sheet_template == "test_income_sheet.tex"
    assert config.DEBUG is True


def test_exceptin_raised():
    """It raises an exception if the config file is not found."""
    with pytest.raises(Exception):
        Config("/path/does/not/exist/config")
