from pacioli.income_statement import IncomeStatement


def test_process_account():
    report = IncomeStatement(config_file="tests/resources/sample_config.yml")
    assert {
        "Salary": 4913,
        "Interest": 40,
        "income_total": 4953,
    } == report.process_accounts("Income", start_date="2020/2/1", end_date="2020/3/31")
