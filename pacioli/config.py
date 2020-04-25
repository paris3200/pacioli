""" Provides the configuration for the Pacaoli module. """
import os

import yaml


class Config:
    """
    Reads the configuration from config file.

    Parameters
    ----------
    config_file: str
        File path of config file.
    """

    def __init__(self, config_file=None):

        xdg_config = os.environ.get("XDG_CONFIG_HOME")

        if not config_file:
            if not xdg_config:
                config_file = "~/.config/pacioli/config.yml"
            else:
                config_file = xdg_config + "/pacioli/config.yml"

        # Get the absolute file path
        self.config_file = os.path.expanduser(config_file)
        if not os.path.isfile(self.config_file):
            raise Exception("Config file not found")

        self.parse_config()

    def parse_config(self):
        """
        Reads the config file and imports settings.

        """
        with open(self.config_file) as config:
            data = yaml.load(config, Loader=yaml.FullLoader)
            self.journal_file = data["journal_file"]
            effective = data["effective"]
            if effective:
                self.effective = "--effective"

            # Process account mappings
            self.current_assets = data["Current Assets"]
            self.longterm_assets = data["Longterm Assets"]
            self.unsecured_liabilities = data["Unsecured Liabilities"]
