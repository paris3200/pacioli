import click
from pacioli.pacioli import Pacioli


@click.group()
@click.option(
    "--config",
    "-c",
    default="~/.config/pacioli/config.yml",
    help="Path of config file.",
)
@click.pass_context
def cli(ctx, config):
    """
    Pacioli generates beautiful LaTeX financial reports from Ledger CLI journal
    files.
    """
    ctx.ensure_object(dict)
    ctx.obj["pacioli"] = Pacioli(config_file=config)


@cli.command()
@click.option(
    "--out-file", "-o", default="-", help="Path of file to write report results."
)
@click.option("--end-date", "-e", default="", help="End date for transactions.")
@click.pass_context
def balance_sheet(ctx, out_file, end_date):
    """
    Run a balance report using the  account mappings defined in the config file.
    """
    pacioli = ctx.obj["pacioli"]
    click.echo(pacioli.balance_sheet(date=end_date))


if __name__ == "__main__":
    cli()
