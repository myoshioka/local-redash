import json
from typing import Callable, TypeAlias, Union

import sqlfluff
from black import FileMode, format_file_contents
from local_redash.models.redash_client import DataSourceType, SqlFormatDialects

ResultDataRow: TypeAlias = dict[str, Union[str, int, dict]]
ResultData: TypeAlias = list[ResultDataRow]


class Command:

    def __init__(self) -> None:
        pass

    def execute(self, *args) -> ResultData:
        raise NotImplementedError()

    def filter_columns(self, result_data: ResultData,
                       columns: set[str]) -> ResultData:

        check: Callable[[tuple[str, str | int]],
                        bool] = lambda item: item[0] in columns
        return list(
            map(lambda row: dict(filter(check, row.items())), result_data))

    def sort_records(self, result_data: ResultData,
                     column_name: str) -> ResultData:
        return sorted(result_data,
                      key=lambda row: json.dumps(row[column_name]))

    def format_query(self, query_str: str,
                     data_source_type: DataSourceType) -> str:

        if data_source_type == DataSourceType.PYTHON:
            return self.format_python_code(query_str)
            # return query_str
        else:
            return self.format_sql(query_str, data_source_type)

    def format_sql(self, query_str: str,
                   data_source_type: DataSourceType) -> str:
        dialect = SqlFormatDialects.from_datasource_type(data_source_type)

        return sqlfluff.fix(
            query_str,
            dialect=dialect,
        )

    def format_python_code(self, python_code: str) -> str:
        return format_file_contents(python_code, fast=False, mode=FileMode())
