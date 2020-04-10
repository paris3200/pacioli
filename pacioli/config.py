""" Provides the configuration for the Pacaoli module. """ import errno
import json
import os

import yaml


class Config:
    """
    Reads the configuration from config file.

    Parameters
    ----------
    config_file: str
        File path of config file.
    profile: str
        Profile name from config file to be used
    """

    def __init__(self, config_file=None, profile="default"):

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

        self.parse_config(profile)

    def parse_config(self, profile):
        """
        Reads the config file and imports settings.

        Parameters
        ----------
        profile: str
            Profile name from config file to be used
        """

        with open(self.config_file) as config:
            data = yaml.load(config, Loader=yaml.FullLoader)
            self.file = data["file"]
            self.effective = data["effective"]
            # TODO Catch NameError
            if profile:
                self.profile = data["profile"][profile]
