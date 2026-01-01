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
    assert config.effective is None
    assert config.cleared is None
    assert config.journal_file == "tests/resources/sample_ledger.ldg"
    assert config.balance_sheet_template == "test_balance_sheet.tex"
    assert config.income_sheet_template == "test_income_sheet.tex"
    assert config.DEBUG is True


def test_exceptin_raised():
    """It raises an exception if the config file is not found."""
    with pytest.raises(Exception):
        Config("/path/does/not/exist/config")


def test_xdg_config_home_is_used_if_no_config_file(monkeypatch):
    """It looks for config file in XDG_CONFIG_HOME."""
    monkeypatch.setenv("XDG_CONFIG_HOME", "/awesome/path")
    assert Config.get_config_path() == "/awesome/path/pacioli/config.yml"


def test_xdg_config_home_not_set_defaults_to_config(monkeypatch):
    """If XDG_CONFIG_HOME not set and there is no config file path passed then ~/.config/pacioli is used."""
    monkeypatch.setenv("XDG_CONFIG_HOME", "")
    assert Config.get_config_path() == "~/.config/pacioli/config.yml"


def test_init_config_none(monkeypatch):
    """It defaults looks for config file if none passed."""
    monkeypatch.setenv("XDG_CONFIG_HOME", "tests/resources")
    config = Config()
    assert config.config_file == "tests/resources/pacioli/config.yml"
