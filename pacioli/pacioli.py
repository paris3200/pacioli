import os
import subprocess
import re

import jinja2
from jinja2 import Template

from pacioli.config import Config


class Pacioli:

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
        output = subprocess.run(["ledger", "-f",
            self.config.journal_file, "bal", account, "-e", self.date,
            self.config.effective], stdout=subprocess.PIPE)
        output = output.stdout.decode('utf-8')
        output = output.replace(',', '')
        return round(float(re.search("\d+(?:.(\d+))?", output).group(0)))

    def compile_template(self, **kwargs):
        template = self.latex_jina_env.get_template("balance_sheet.tex")
        print(template.render(checking=checking, \
                savings=savings, \
                current_assets=current_assets, \
                escrow=escrow, \
                realestate=realestate, \
                investments=investments, \
                receivable=receivable, \
                longterm_assets=longterm_assets, \
                total_assets=total_assets))


if __name__ == "__main__":

    pacioli = Pacioli()

    checking = pacioli.get_balance("Assets:Current:SECU:Checking")
    savings = pacioli.get_balance("Assets:Current:SECU:Savings")
    current_assets = round(checking) + round(savings)
    current_assets = 10

    escrow = pacioli.get_balance("Assets:Noncurrent:SECU:Escrow")
    realestate = pacioli.get_balance("Assets:Noncurrent:House")
    investments = pacioli.get_balance("Assets:Noncurrent:Retirement")
    receivable = pacioli.get_balance("Assets:Noncurrent:Parisleatherworks")


    longterm_assets = round(escrow) + round(realestate)+ round(investments) + round(receivable)
    total_assets = current_assets + longterm_assets

    pacioli.compile_template()


