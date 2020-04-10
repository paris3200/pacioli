import os
import subprocess
import re

import jinja2
from jinja2 import Template


class Reporter:

    def __init__(self):

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

        self.file = "/home/jason/documents/finances/ledger/ledger.ldg"
        self.date = "2020/3/31"
        self.effective = "--effective"

    def get_balance(self, account):
        output = subprocess.run(["ledger", "-f",
            self.file, "bal", account, "-e", self.date, self.effective], stdout=subprocess.PIPE)
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

    ledger = Reporter()

    checking = ledger.get_balance("Assets:Current:SECU:Checking")
    savings = ledger.get_balance("Assets:Current:SECU:Savings")
    current_assets = round(checking) + round(savings)
    current_assets = 10

    escrow = ledger.get_balance("Assets:Noncurrent:SECU:Escrow")
    realestate = ledger.get_balance("Assets:Noncurrent:House")
    investments = ledger.get_balance("Assets:Noncurrent:Retirement")
    receivable = ledger.get_balance("Assets:Noncurrent:Parisleatherworks")


    longterm_assets = round(escrow) + round(realestate)+ round(investments) + round(receivable)
    total_assets = current_assets + longterm_assets

    ledger.compile_template()


