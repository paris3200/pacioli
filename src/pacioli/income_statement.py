"""
The income_statement module process the data into a formatted Income Statement.

Classes
-------
IncomeStatement
"""

import re

from pacioli.pacioli import Pacioli, logging
from pacioli.utils import format_balance


class IncomeStatement(Pacioli):
    """
    A class to create the Income Statement.

    Methods
    -------
    print_report(start_date, end_date)
        Returns income state for the time period specified.
    """

    def __init__(self, config_file) -> None:
        """Read template path from config file.

        Parameters
        ----------
        config_file: str
            Path to config file.
        """
        Pacioli.__init__(self, config_file)
        self.template = self.config.income_sheet_template

    def print_report(self, start_date, end_date) -> str:
        """Generate the income statment.

        Returns an income statement for the period beginning on start_date and
        up to, but not including transactions on the end_date.

        Parameters
        ----------
        start_date: str
        end_date: str

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

        income = self.process_accounts("Income", start_date, end_date)
        result["income_total"] = income.pop("income_total", 0)
        result["income"] = income

        expenses = self.process_accounts("Expenses", start_date, end_date)
        result["expenses_total"] = expenses.pop("expenses_total", 0)
        result["expenses"] = expenses

        if result["income_total"] == 0 and not income:
            logging.warning("No income accounts found for the specified period")
        if result["expenses_total"] == 0 and not expenses:
            logging.warning("No expense accounts found for the specified period")

        result["net_income"] = result["income_total"] - result["expenses_total"]

        logging.debug(result)
        return self.render_template(self.template, format_balance(result))

    def process_accounts(self, account, start_date, end_date):
        """Proccess acount balances within time period.

        Return a dictionary of all sub account names and their corresponding
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
            "--depth",
            "2",
        ]

        if self.effective:
            ledger_command.append("--effective")

        if self.cleared:
            ledger_command.append("--cleared")

        if self.market:
            ledger_command.extend(self.market.split())

        output = self.run_system_command(ledger_command).splitlines()
        account_name = account
        result = {}
        for i in output:
            i = i.replace(",", "")
            account = re.search(r"([a-zA-Z]+[a-zA-Z ]*[a-zA-Z])+", i)
            if account is not None:
                balance_match = re.search(r"\d+(?:.(\d+))?", i)
                if not balance_match:
                    raise ValueError(f"Unable to parse balance from ledger output line: {i}")
                if account.group(0) == account_name:
                    result[account_name.lower() + "_total"] = round(float(balance_match.group(0)))
                else:
                    account = account.group(0)
                    result[account] = round(float(balance_match.group(0)))

        return result
