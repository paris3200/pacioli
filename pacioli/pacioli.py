import os
import subprocess
import re
import jinja2

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

        self.latex_jina_env = jinja2.Environment(
            block_start_string="BLOCK{",
            block_end_string="}",
            variable_start_string="\VAR{",
            variable_end_string="}",
            comment_start_string="\#{",
            comment_end_string="}",
            line_statement_prefix="%%",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(os.path.abspath(".")),
        )

        self.config = Config(config_file)
        self.date = "2020/3/31"

    def balance_sheet(self, date):
        """
        Generates the balance sheet report as a tex file.

        Parameters
        ----------
        date: str
            End date for ledger balances.

        Returns
        -------
        str
            Balance sheet in tex format.
        """
        current_assets = self.process_category(
            self.config.current_assets, "current_assets", date=date
        )
        longterm_assets = self.process_category(
            self.config.longterm_assets, "longterm_assets", date=date
        )
        secured_liabilities = self.process_category(
            self.config.secured_liabilities, "secured_liabilities", date=date
        )
        unsecured_liabilities = self.process_category(
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
        ledger = {}
        ledger.update({"total_assets": total_assets})
        ledger.update({"total_liabilities": total_liabilities})

        ledger.update({"title": self.config.title})
        ledger.update({"date": date})
        ledger.update(current_assets)
        ledger.update(longterm_assets)
        ledger.update(secured_liabilities)
        ledger.update(unsecured_liabilities)

        return self.compile_template(ledger)

    def income_statement(self, start_date, end_date):
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
        pass

    def get_balance(self, account, date):
        """
        Get's the account balance from Ledger of account and rounds it to a
        whole number.

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

        try:
            output = subprocess.run(
                [
                    "ledger",
                    "-f",
                    self.config.journal_file,
                    "bal",
                    account,
                    "-e",
                    date,
                    self.config.effective,
                ],
                stdout=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as error:
            print("error code", error.returncode, error.output)
        output = output.stdout.decode("utf-8")
        output = output.replace(",", "")
        if output != "":
            return round(float(re.search("\d+(?:.(\d+))?", output).group(0)))
        return 0

    def process_category(self, category, category_name, date):
        """

        Returns a dictionary of account names and their corresponding balances
        as of the date along with the total value of category.

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
        dict
            Short account names and their balances.
        """
        total = 0
        result = {}
        for account in category:
            name = self.get_account_name(account)
            balance = self.get_balance(account, date)
            total += balance
            result[name] = balance

        name = f"{category_name}_total"
        result[name] = total
        return result

    def get_account_name(self, account):
        """
        Returns the account name from the full account path in lower case with
        spaces replaced with a \'_\".

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

    def compile_template(self, account_mappings):
        """

        Parameters
        ----------
        account_mappings: dict
            The variable name in the template matched to the corresponding
            account balance.

        Returns
        -------
        str
            Processed LaTeX document with account totals.

        """
        template = self.latex_jina_env.get_template(self.config.balance_sheet_template)
        return template.render(account_mappings)
