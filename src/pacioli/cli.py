import click

from pacioli import __version__
from pacioli.balance_sheet import BalanceSheet
from pacioli.cash_flow_statement import CashFlowStatement
from pacioli.income_statement import IncomeStatement
from pacioli.utils import month_to_dates, period_to_dates


@click.group()
@click.version_option(version=__version__, prog_name="pacioli")
@click.option(
    "--config",
    "-c",
    default="~/.config/pacioli/config.yml",
    help="Path of config file.",
)
@click.pass_context
def cli(ctx, config) -> None:
    """
    Pacioli generates LaTeX financial reports from Ledger CLI journal
    files.
    """
    ctx.ensure_object(dict)
    ctx.obj["balance_sheet"] = BalanceSheet(config_file=config)
    ctx.obj["income_statement"] = IncomeStatement(config_file=config)
    ctx.obj["cash_flow_statement"] = CashFlowStatement(config_file=config)


@cli.command()
@click.argument("out-file", type=click.Path(allow_dash=True), default="-")
@click.option("--end-date", "-e", default="", help="Limit the report to transactions before date.")
@click.pass_context
def balance_sheet(ctx, out_file, end_date) -> None:
    """
    Run a balance report using the  account mappings defined in the config file.

    OUT_FILE is the path to the file to write the tex file. Defaults to standard
    output if not specified. Use '-' for explicit stdout.
    """
    balance_sheet = ctx.obj["balance_sheet"]

    if out_file != "-":
        with click.open_file(out_file, "w") as f:
            f.write(balance_sheet.print_report(date=end_date))
    else:
        click.echo(balance_sheet.print_report(date=end_date))


@cli.command()
@click.option("--begin-date", "-b", default="", help="Start date for transactions.")
@click.option("--end-date", "-e", default="", help="Limit the report to transactions BEFORE date.")
@click.option(
    "--month", "-m", default="", help="(DEPRECATED: use --period instead) Limit report to month."
)
@click.option(
    "--period",
    "-p",
    default="",
    help="Period description (e.g., 'last month', 'Jan to Mar', 'Jan 2024 to Mar 2024').",
)
@click.argument("out-file", type=click.Path(allow_dash=True), default="-")
@click.pass_context
def income_statement(ctx, begin_date, end_date, month, period, out_file) -> None:
    """
    Run a income statement for a set time period.

    OUT_FILE is the path to the file to write the tex file. Defaults to standard
    output if not specified. Use '-' for explicit stdout.
    """
    income_statement = ctx.obj["income_statement"]

    if begin_date == end_date == month == period == "":
        raise click.UsageError("Please enter a valid begin-date and end-date, month, or period.")
    elif period != "":
        begin_date, end_date = period_to_dates(period)
    elif month != "":
        click.echo(
            "Warning: --month is deprecated. Use --period instead (e.g., --period 'January').",
            err=True,
        )
        begin_date, end_date = month_to_dates(month)

    report = income_statement.print_report(begin_date, end_date)
    if out_file != "-":
        with click.open_file(out_file, "w") as f:
            f.write(report)
    else:
        click.echo(report)


@cli.command()
@click.option("--begin-date", "-b", default="", help="Start date for transactions.")
@click.option("--end-date", "-e", default="", help="Limit the report to transactions BEFORE date.")
@click.option(
    "--month", "-m", default="", help="(DEPRECATED: use --period instead) Limit report to month."
)
@click.option(
    "--period",
    "-p",
    default="",
    help="Period description (e.g., 'last month', 'Jan to Mar', 'Jan 2024 to Mar 2024').",
)
@click.argument("out-file", type=click.Path(allow_dash=True), default="-")
@click.pass_context
def cash_flow_statement(ctx, begin_date, end_date, month, period, out_file) -> None:
    """
    Run a cash flow statement for a set time period.

    OUT_FILE is the path to the file to write the tex file. Defaults to standard
    output if not specified. Use '-' for explicit stdout.
    """
    cash_flow_statement = ctx.obj["cash_flow_statement"]

    if begin_date == end_date == month == period == "":
        raise click.UsageError("Please enter a valid begin-date and end-date, month, or period.")
    elif period != "":
        begin_date, end_date = period_to_dates(period)
    elif month != "":
        click.echo(
            "Warning: --month is deprecated. Use --period instead (e.g., --period 'January').",
            err=True,
        )
        begin_date, end_date = month_to_dates(month)

    report = cash_flow_statement.print_report(begin_date, end_date)
    if out_file != "-":
        with click.open_file(out_file, "w") as f:
            f.write(report)
    else:
        click.echo(report)
