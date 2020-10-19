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
@click.argument("out-file", type=click.Path(allow_dash=True))
@click.option("--end-date", "-e", default="", help="End date for transactions.")
@click.pass_context
def balance_sheet(ctx, out_file, end_date):
    """
    Run a balance report using the  account mappings defined in the config file.

    OUT_FILE is the path to the file to write the tex file.  Use '-' to print
    to standard output.
    """
    pacioli = ctx.obj["pacioli"]

    if out_file != "-":
        with click.open_file(out_file, "w") as f:
            f.write(pacioli.balance_sheet(date=end_date))
    else:
        click.echo(pacioli.balance_sheet(date=end_date))


@cli.command()
@click.option("--begin-date", "-b", default="", help="Begin date of time period.")
@click.option("--end-date", "-e", default="", help="End date of time period.")
@click.argument("out-file", type=click.Path(allow_dash=True))
@click.pass_context
def income_statement(ctx, begin_date, end_date, out_file):
    pacioli = ctx.obj["pacioli"]
    if out_file != "-":
        with click.open_file(out_file, "w") as f:
            f.write(pacioli.income_statement(begin_date, end_date))
    else:
        click.echo(pacioli.income_statement(begin_date, end_date))


if __name__ == "__main__":
    cli()
