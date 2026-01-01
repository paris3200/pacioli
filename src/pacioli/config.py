"""Read and process the config file.

Classes
-------
Config
"""

import os

import yaml


class Config:
    """Reads the configuration settings from config file."""

    def __init__(self, config_file=None):
        """Verify the path for the config file.

        Parameters
        ----------
        config_file: str
            File path of config file.
        """
        if not config_file:
            config_file = self.get_config_path()

        # Get the absolute file path
        self.config_file = os.path.expanduser(config_file)
        self.template_dir = os.path.dirname(self.config_file)

        if not os.path.isfile(self.config_file):
            raise FileNotFoundError(f"Config file not found: {self.config_file}")

        self.parse_config()

    @staticmethod
    def get_config_path() -> str:
        """Get the config file path based on XDG_CONFIG_HOME.

        If XDG_CONFIG_HOME not set defaults to ~/.config/pacioli/config.yml.

        Return
        ------
        str
            File path of config file.
        """
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if not xdg_config:
            config_file = "~/.config/pacioli/config.yml"
        else:
            config_file = xdg_config + "/pacioli/config.yml"

        return config_file

    def parse_config(self):
        """Read the config file and import settings."""
        with open(self.config_file) as config:
            data = yaml.safe_load(config)
            self.DEBUG = data["DEBUG"]
            self.journal_file = data["journal_file"]
            self.balance_sheet_template = os.path.expanduser(data["balance_sheet_template"])

            self.income_sheet_template = os.path.expanduser(data["income_sheet_template"])
            self.cash_flow_template = os.path.expanduser(data["cash_flow_template"])
            if data["effective"]:
                self.effective = "--effective"
            else:
                self.effective = None

            if data["cleared"]:
                self.cleared = "--cleared"
            else:
                self.cleared = None

            # Market value conversion for commodities
            if "market" in data and data["market"]:
                if isinstance(data["market"], str):
                    # If market is a currency string like "USD" or "$"
                    self.market = f"--exchange {data['market']}"
                else:
                    # If market is True/boolean, use default --market flag
                    self.market = "--market"
            else:
                self.market = None

            # Process Balance Sheet account mappings
            self.current_assets = data["Current Assets"]
            self.longterm_assets = data["Longterm Assets"]
            self.unsecured_liabilities = data["Unsecured Liabilities"]
            self.secured_liabilities = data["Secured Liabilities"]

            # Process Cash Flow Statement account mappings
            self.cash_accounts = data["Cash Accounts"]
            self.operating_activities = data["Operating Activities"]
            self.investing_activities = data["Investing Activities"]
            self.financing_activities = data["Financing Activities"]

            self.title = data["title"]
