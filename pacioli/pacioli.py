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

    def get_balance(self, account):
        """
        Get's the account balance from Ledger of account and rounds it to a
        whole number.

        Parameters
        ----------
        account: str
            The account name in the ledger file.
        """
        output = subprocess.run(
            [
                "ledger",
                "-f",
                self.config.journal_file,
                "bal",
                account,
                "-e",
                self.date,
                self.config.effective,
            ],
            stdout=subprocess.PIPE,
        )
        output = output.stdout.decode("utf-8")
        output = output.replace(",", "")
        return round(float(re.search("\d+(?:.(\d+))?", output).group(0)))

    def compile_template(self, **kwargs):
        template = self.latex_jina_env.get_template("pacioli/balance_sheet.tex")

        return template.render(kwargs)
        # print(
        #    template.render(
        #        checking=checking,
        #        savings=savings,
        #        current_assets=current_assets,
        #        escrow=escrow,
        #        realestate=realestate,
        #        investments=investments,
        #        receivable=receivable,
        #        longterm_assets=longterm_assets,
        #        total_assets=total_assets,
        #    )
        # )
