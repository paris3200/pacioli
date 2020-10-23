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

    def render_balance_sheet(self, date):
        """
        Generates the balance sheet from the category mappings in the config
        file.

        Parameters
        ----------
        date: str
            End date for ledger balances.

        Returns
        -------
        str
            Balance sheet in tex format.
        """
        current_assets = self.process_account_list(
            self.config.current_assets, "current_assets", date=date
        )
        longterm_assets = self.process_account_list(
            self.config.longterm_assets, "longterm_assets", date=date
        )
        secured_liabilities = self.process_account_list(
            self.config.secured_liabilities, "secured_liabilities", date=date
        )
        unsecured_liabilities = self.process_account_list(
            self.config.unsecured_liabilities, "unsecured_liabilities", date=date
        )

        total_assets = (
            current_assets["current_assets_total"]
            + longterm_assets["longterm_assets_total"]
        )
        total_liabilities = (
            secured_liabilities["secured_liabilities_total"]
            + unsecured_liabilities["unsecured_liabilities_total"]
        )
        ledger = {
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "title": self.title,
            "date": date,
        }

        ledger.update(current_assets)
        ledger.update(longterm_assets)
        ledger.update(secured_liabilities)
        ledger.update(unsecured_liabilities)

        return self.render_template("balance", self.format_balance(ledger))

    def render_income_statement(self, start_date, end_date):
        """
        Returns an income statement for the period beginning on start_date and
        ending on end_date.

        Parameters
        ----------
        start_date: str
            The start date of the time period.
        end_date: str
            The end date of the time period.

        Returns
        -------
        str
            The income statement in tex format.

        """
        result = {
            "title": self.title,
            "start_date": start_date,
            "end_date": end_date,
        }

        income = self.process_account("Income", start_date, end_date)
        result["income_total"] = income.pop("income_total")
        result["income"] = income

        expenses = self.process_account("Expenses", start_date, end_date)
        result["expenses_total"] = expenses.pop("expenses_total")
        result["expenses"] = expenses

        net_gain = result["income_total"] - result["expenses_total"]
        result["net_gain"] = self.format_net_gain(net_gain)

        logging.debug(result)
        return self.render_template("income", self.format_balance(result))

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

    def process_account(self, account, start_date, end_date):
        """
        Returns a dictionary of all sub account names and their corresponding
        balances for the time period.

        Parameters
        ----------
        account:str
            Top level account name, i.e 'Income'.
        start_date: str
        end_date: str

        Returns
        -------
        dict
            Short account names and their balances.

        """
        ledger_command = [
            "ledger",
            "-f",
            self.journal_file,
            "bal",
            account,
            "-b",
            start_date,
            "-e",
            end_date,
            self.effective,
            "--depth",
            "2",
            self.cleared,
        ]

        output = self.run_system_command(ledger_command).splitlines()
        account_name = account
        result = {}
        for i in output:
            i = i.replace(",", "")
            account = re.search(r"([a-zA-Z]+[a-zA-Z ]*[a-zA-Z])+", i)
            if account is not None:
                if account.group(0) == account_name:
                    result[account_name.lower() + "_total"] = round(
                        float(re.search(r"\d+(?:.(\d+))?", i).group(0))
                    )
                else:
                    account = account.group(0)
                    result[account] = round(
                        float(re.search(r"\d+(?:.(\d+))?", i).group(0))
                    )

        return result

    def process_account_list(self, category, category_name, date):
        """

        Returns a dictionary of account names and their corresponding balances
        as of the date along with the total value of category from a known list
        of accounts.

        Parameters
        ----------
        category: list
            List of full account names in a category.
        cateogry_name: str
            The parent acount name, i.e 'Current Assets'.
        date: str
            The end date for the balance.

        Returns
        -------
        """
        total = 0
        result = {}
        for account in category:
            name = self.get_account_short_name(account)
            balance = self.get_balance(account, date)
            total += balance
            result[name] = balance

        name = f"{category_name}_total"
        result[name] = total
        return result

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
            return f"{int_balance:n}"

        if isinstance(int_balance, dict):
            for account, balance in int_balance.items():
                if isinstance(balance, dict):
                    self.format_balance(balance)
                elif isinstance(balance, int):
                    int_balance[account] = f"{balance:n}"

        return int_balance

    def format_net_gain(self, net_gain):
        """
        If the input_number is negative, it returns the absolute value of the
        number as string enclosed in parenttheses.

        Paramaters
        ----------
        net_gain: int
            Number to be formatted

        Returns
        -------
        Str
            Net gain as a string.  If negative, enclosed in parentheses.
        """
        if net_gain < 0:
            return "(" + self.format_balance(abs(net_gain)) + ")"

        return self.format_balance(net_gain)

    def render_template(self, report_type, account_mappings):
        """
        Executes the jinja template.

        Parameters
        ----------
        report_type: str
            (balance, income)
        account_mappings: dict
            The variable name in the template matched to the corresponding
            account balance.

        Returns
        -------
        str
            Processed LaTeX document with account totals.

        """
        try:
            if report_type == "balance":
                template = self.latex_jinja_env.get_template(
                    self.config.balance_sheet_template
                )
            elif report_type == "income":
                template = self.latex_jinja_env.get_template(
                    self.config.income_sheet_template
                )
        except jinja2.exceptions.TemplateNotFound as error:
            logging.error("Template Not Found", error)
            return None
        logging.debug("Rendering Template: %s", template)
        return template.render(account_mappings)
