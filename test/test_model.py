from local_redash.models.redash_client import DataSourceType, SqlFormatDialects


def test_sql_format_dialects():
    pg = DataSourceType('pg')
    pg_dialects = SqlFormatDialects.from_datasource_type(pg)

    assert pg_dialects == 'postgres'

    python = DataSourceType('python')
    python_dialects = SqlFormatDialects.from_datasource_type(python)

    assert python_dialects == 'ansi'
