import subprocess

from pacioli import __version__
from pacioli.pacioli import Pacioli



def test_version():
    assert __version__ == '0.1.0'


def test_ledger_available():
    "Verify ledger is availabe on the system" 
    output = subprocess.run(["ledger", "--version"], capture_output=True)
    assert output.returncode == 0


def test_get_balance_returns_int():
    pacioli = Pacioli(config_file="tests/resources/sample_config.yml")

    checking = pacioli.get_balance("Assets:Current:Checking")
    assert checking == 3648


