import os
import subprocess
import re
import jinja2
import logging
import locale

from pacioli.config import Config


class Pacioli:
    """
    Pacioli converts a ledger journal file data into a finacial reports
    formatted with LaTex.  The LaTeX reports can then be piped into a LaTeX to
    pdf convertor inorder to generate beautiful, accurate reports.

    Paramaters
    ----------
    config_file: str
        Path to the config file.
    """

    def __init__(self, config_file=None):

        self.config = Config(config_file)

        self.title = self.config.title
        self.effective = self.config.effective
        self.cleared = self.config.cleared
        self.journal_file = self.config.journal_file
        self.latex_jinja_env = self.setup_jinja_env()

        if self.config.DEBUG:
            self.setup_log("debug")

    def setup_jinja_env(self):
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

    def setup_log(self, log_level):
        if log_level == "debug":
            logging.basicConfig(level=logging.DEBUG)

    def run_system_command(self, command):
        try:
            output = subprocess.run(command, stdout=subprocess.PIPE,)
        except subprocess.CalledProcessError as error:
            logging.error("error code", error.returncode, error.output)

        logging.debug(f"System Command:  {command}")
        return output.stdout.decode("utf-8")

    def get_balance(self, account, date):
        """
        Get's the account balance from Ledger of account and rounds it to an
        int.

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
            self.effective,
            self.cleared,
        ]

        output = self.run_system_command(ledger_command)
        output = output.replace(",", "")
        if output != "":
            return round(float(re.search(r"\d+(?:.(\d+))?", output).group(0)))
        return 0

    def get_account_short_name(self, account):
        """
        Returns the account name from the full account path in lower case with
        spaces replaced with a \"_\".

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

    def format_balance(self, int_balance):
        """
        Formats balance using the locale seperators for numbers.

        Parameters
        ----------
        int_balance: (dict, int)


        Returns
        -------
        (dict, int)
           Balance formatted with locale seperator.
        """
        locale.setlocale(locale.LC_ALL, "")

        if isinstance(int_balance, int):
            balance = self.format_negative_numbers(int_balance)
            return f"{balance:n}"

        if isinstance(int_balance, dict):
            for account, balance in int_balance.items():
                if isinstance(balance, dict):
                    self.format_balance(balance)
                elif isinstance(balance, int):
                    balance = self.format_negative_numbers(balance)
                    int_balance[account] = f"{balance:n}"

        return int_balance

    def format_negative_numbers(self, number):
        """
        If the input_number is negative, it returns the absolute value of the
        number as string enclosed in parenttheses.

        Paramaters
        ----------
        number: int
            Number to be formatted

        Returns
        -------
        Str
            Net gain as a string.  If negative, enclosed in parentheses.
        """
        if number < 0:
            return "(" + self.format_balance(abs(number)) + ")"

        return number
