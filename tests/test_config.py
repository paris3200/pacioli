"""
Test the Config Class
"""
from pacioli.config import Config


def test_profile_set():
    config = Config("tests/resources/sample_config.yml")
    assert config.effective == "--effective"
    assert config.journal_file == "tests/resources/sample_ledger.ldg"
