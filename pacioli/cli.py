import click
from pacioli.pacioli import Pacioli


@click.command()
@click.option(
    "--config",
    "-c",
    default="~/.config/pacioli/config.yml",
    help="Path of config file.",
)
@click.option(
    "--out-file", "-o", default="-", help="Path of file to write report results."
)
@click.option(
    "--balance-sheet",
    is_flag=True,
    help="Run a balance report using the  account mappings defined in the config file.",
)
def cli(config, out_file, balance_sheet):
    """
    Pacioli generates beautiful LaTeX financial reports from Ledger CLI journal
    files.
    """
    pacioli = Pacioli(config_file=config)

    if balance_sheet:
        click.echo(pacioli.balance_sheet(date="2020/3/31"))


if __name__ == "__main__":
    cli()
