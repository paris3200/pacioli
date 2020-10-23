import jinja2

from pacioli.pacioli import Pacioli, logging


class BalanceSheet(Pacioli):
    def __init__(self, config_file):
        Pacioli.__init__(self, config_file)

    def print_report(self, date):
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
        current_assets = self.process_accounts(
            self.config.current_assets, "current_assets", date=date
        )
        longterm_assets = self.process_accounts(
            self.config.longterm_assets, "longterm_assets", date=date
        )
        secured_liabilities = self.process_accounts(
            self.config.secured_liabilities, "secured_liabilities", date=date
        )
        unsecured_liabilities = self.process_accounts(
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

        return self.render_template(self.format_balance(ledger))

    def process_accounts(self, category, category_name, date):
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

    def render_template(self, account_mappings):
        """
        Executes the jinja template.

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
        try:
            template = self.latex_jinja_env.get_template(
                self.config.balance_sheet_template
            )
        except jinja2.exceptions.TemplateNotFound as error:
            logging.error("Template Not Found", error)
            return None
        logging.debug("Rendering Template: %s", template)
        return template.render(account_mappings)
