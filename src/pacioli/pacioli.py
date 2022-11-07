import locale
import logging
import os
import re
import subprocess

import jinja2
from pacioli.config import Config


class Pacioli:
    """Creates beautiful finacial reports.

    Pacioli converts a ledger journal file data into a finacial reports
    formatted with LaTex.  The LaTeX reports can then be piped into a LaTeX to
    pdf convertor inorder to generate beautiful, accurate reports.
    """

    def __init__(self, config_file=None) -> None:
        """Set configuration from Config.

        Paramaters
        ----------
        config_file: str
            Path to the config file.
        """
        self.config = Config(config_file)

        self.title = self.config.title
        self.effective = self.config.effective
        self.cleared = self.config.cleared
        self.journal_file = self.config.journal_file
        self.latex_jinja_env = self.setup_jinja_env()

        if self.config.DEBUG:
            self.setup_log("DEBUG")

    def setup_jinja_env(self):
        """Create jinja2 environment."""
        return jinja2.Environment(
            block_start_string="BLOCK{",
            block_end_string="}",
            variable_start_string=r"\VAR{",
            variable_end_string="}",
            comment_start_string=r"\#{",
            comment_end_string="}",
            line_statement_prefix="%%",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(os.path.abspath(self.config.template_dir)),
        )

    def setup_log(self, log_level) -> None:
        """Create and configure logger.

        Parameters
        ----------
        log_level: str
            Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

    def run_system_command(self, command) -> str:
        """Run a system command.

        Parameters
        ----------
        command: str
            System command to be run.


        Returns
        -------
        str: The output of the command.
        """
        try:
            output = subprocess.run(
                command,
                stdout=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as error:
            self.logger.error("error code", error.returncode, error.output)
            raise

        self.logger.debug(f"System Command:  {command}")
        return output.stdout.decode("utf-8")

    def render_template(self, template, account_mappings) -> str:
        """Execute the jinja template.

        Parameters
        ----------
        template: str
            Path to template file.
        account_mappings: dict
            The variable name in the template matched to the corresponding
            account balance.

        Returns
        -------
        str
            Processed LaTeX document with account totals.

        """
        try:
            template = self.latex_jinja_env.get_template(template)
        except jinja2.exceptions.TemplateNotFound as error:
            raise FileNotFoundError("Template not Found: ", error)

        return template.render(account_mappings)

    def get_balance(self, account, date) -> int:
        """Return account balance as rounded, signed int.

        Parameters
        ----------
        account: str
            The full account path (e.g. Assets:Current:Checking) of the ledger
            account.
        date: str
            The end date for the balance.

        Returns
        -------
        int
            Rounded account balance
        """
        ledger_command = [
            "ledger",
            "-f",
            self.journal_file,
            "bal",
            account,
            "--end",
            date,
        ]

        if self.effective:
            ledger_command.append("--effective")

        if self.cleared:
            ledger_command.append("--cleared")

        output = self.run_system_command(ledger_command)
        output = output.replace(",", "")
        if output == "":
            bal = 0
        else:
            bal = round(float(re.search(r"\d+(?:.(\d+))?", output).group(0)))
            if "$-" in output:
                bal = int(f"-{bal}")
        return bal

    def get_account_short_name(self, account) -> str:
        """Get the short account name.

        Returns the account name from the full account path in lower case with
        spaces replaced with a '_'.

        Parameters
        ----------
        account: str
            Full account path

        Returns
        -------
        str
            Account name
        """
        name = account.split(":")[-1].lower()
        return name.replace(" ", "_")
