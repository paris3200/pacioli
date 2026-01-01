"""
The cash_flow_statement module processes data into a formatted Cash Flow Statement.

Classes
-------
CashFlowStatement
"""

from typing import Dict

from pacioli.pacioli import Pacioli, logging
from pacioli.utils import format_balance


class CashFlowStatement(Pacioli):
    """
    A class to create the Cash Flow Statement using the direct method.

    Methods
    -------
    print_report(start_date, end_date)
        Returns cash flow statement for the time period specified.
    """

    def __init__(self, config_file) -> None:
        """Read template path from config file.

        Parameters
        ----------
        config_file: str
            Path to config file.
        """
        Pacioli.__init__(self, config_file)
        self.template = self.config.cash_flow_template

    def print_report(self, start_date, end_date) -> str:
        """Generate the cash flow statement.

        Returns a cash flow statement for the period beginning on start_date and
        up to, but not including transactions on the end_date.

        Parameters
        ----------
        start_date: str
            Start date for the reporting period (YYYY/MM/DD format)
        end_date: str
            End date for the reporting period (YYYY/MM/DD format)

        Returns
        -------
        str
            The cash flow statement in tex format.
        """
        result = {
            "title": self.title,
            "start_date": start_date,
            "end_date": end_date,
        }

        # Calculate cash balances
        beginning_cash = self.get_total_cash_balance(start_date)
        ending_cash = self.get_total_cash_balance(end_date)

        # Process activity categories
        operating = self.process_accounts(self.config.operating_activities, start_date, end_date)
        result["operating_activities_total"] = operating.pop("category_total")
        result["operating_activities"] = operating

        investing = self.process_accounts(self.config.investing_activities, start_date, end_date)
        result["investing_activities_total"] = investing.pop("category_total")
        result["investing_activities"] = investing

        financing = self.process_accounts(self.config.financing_activities, start_date, end_date)
        result["financing_activities_total"] = financing.pop("category_total")
        result["financing_activities"] = financing

        # Calculate totals
        result["net_change_in_cash"] = (
            result["operating_activities_total"]
            + result["investing_activities_total"]
            + result["financing_activities_total"]
        )
        result["beginning_cash"] = beginning_cash
        result["ending_cash"] = ending_cash

        # Verification (for debugging)
        calculated_ending = beginning_cash + result["net_change_in_cash"]
        if calculated_ending != ending_cash:
            self.logger.warning(
                f"Cash reconciliation mismatch: calculated {calculated_ending} "
                f"vs actual {ending_cash}"
            )

        logging.debug(result)
        return self.render_template(self.template, format_balance(result))

    def get_total_cash_balance(self, date) -> int:
        """Calculate total cash balance as of a specific date.

        Sums all accounts defined in Cash Accounts configuration.

        Parameters
        ----------
        date: str
            Date for balance calculation (YYYY/MM/DD format)

        Returns
        -------
        int
            Total cash balance
        """
        total = 0
        for account in self.config.cash_accounts:
            total += self.get_balance(account, date)
        return total

    def process_accounts(self, category, start_date, end_date) -> dict[str, int]:
        """Process account cash flow changes within time period.

        Uses Ledger's --related flag to get only cash-basis transactions.

        Parameters
        ----------
        category: list
            List of full account paths to process
        start_date: str
            Start date (YYYY/MM/DD format)
        end_date: str
            End date (YYYY/MM/DD format)

        Returns
        -------
        dict
            Short account names and their net cash flow changes
        """
        total = 0
        result = {}

        # Query cash accounts with --related to get only cash-basis transactions
        ledger_command = [
            "ledger",
            "-f",
            self.journal_file,
            "bal",
            "--related",
            "-b",
            start_date,
            "-e",
            end_date,
            "--format",
            "%(account)|%(quantity(amount))\n",
        ]

        # Add cash accounts to query
        for cash_account in self.config.cash_accounts:
            ledger_command.append(cash_account)

        if self.effective:
            ledger_command.append("--effective")
        if self.cleared:
            ledger_command.append("--cleared")
        if self.market:
            ledger_command.extend(self.market.split())

        # Get all cash-related transactions
        output = self.run_system_command(ledger_command)

        # Parse output and filter for accounts in this category
        for line in output.strip().split("\n"):
            if not line or "|" not in line:
                continue

            account, amount_str = line.split("|", 1)
            account = account.strip()

            # Check if this account matches any in our category
            for category_account in category:
                if account.startswith(category_account):
                    try:
                        amount = round(float(amount_str.strip()))
                    except ValueError:
                        continue

                    name = self.get_account_short_name(account)
                    # Convert underscores to spaces for display
                    display_name = name.replace("_", " ")

                    # Reverse sign for cash flow presentation
                    # Related accounts show the opposite side of the transaction
                    cash_flow = -amount

                    result[display_name] = cash_flow
                    total += cash_flow
                    break

        result["category_total"] = total
        return result
