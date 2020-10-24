from pacioli.income_statement import IncomeStatement
import locale


def test_process_account():
    report = IncomeStatement(config_file="tests/resources/sample_config.yml")
    assert {
        "Salary": 4913,
        "Interest": 40,
        "income_total": 4953,
    } == report.process_accounts("Income", start_date="2020/2/1", end_date="2020/3/31")


def test_render_template_returns():
    report = IncomeStatement(config_file="tests/resources/sample_config.yml")
    start_date = "2020/2/1"
    end_date = "2020/2/28"
    accounts = {
        "title": report.title,
        "start_date": start_date,
        "end_date": end_date,
    }

    income = report.process_accounts("Income", start_date, end_date)
    accounts["income_total"] = income.pop("income_total")
    accounts["income"] = income

    expenses = report.process_accounts("Expenses", start_date, end_date)
    accounts["expenses_total"] = expenses.pop("expenses_total")
    accounts["expenses"] = expenses

    accounts["net_gain"] = accounts["income_total"] - accounts["expenses_total"]

    result = report.render_template(report.template, report.format_balance(accounts))

    locale.setlocale(locale.LC_ALL, "")
    salary = f"{int(4913):n}"
    income = f"{int(4953):n}"
    expenses = f"{int(3299):n}"

    assert "Acme LLC" in result
    assert f"Salary & {salary} \\" in result
    assert "{Total Income}} & & %s" % income in result
    assert "{Total Expenses}} & & %s \\" % expenses in result
