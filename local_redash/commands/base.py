from typing import Callable, TypeAlias, Union

import sqlfluff
from local_redash.models.redash_client import DataSourceType, SqlFormatDialects

ResultData: TypeAlias = list[dict[str, Union[str, int]]]


class Command:

    def __init__(self) -> None:
        pass

    def execute(self, *args) -> ResultData:
        raise NotImplementedError()

    def filter_columns(self, result_data: ResultData,
                       columns: set[str]) -> ResultData:

        check: Callable[[tuple[str, str | int]],
                        bool] = lambda item: item[0] in columns
        return list(map(lambda x: dict(filter(check, x.items())), result_data))

    def sort_records(self, result_data: ResultData,
                     column_name: str) -> ResultData:
        return sorted(result_data, key=lambda record: record[column_name])

    def format_sql(self, query_str: str,
                   data_source_type: DataSourceType) -> str:
        dialect = SqlFormatDialects.from_datasource_type(data_source_type)

        return sqlfluff.fix(
            query_str,
            dialect=dialect,
        )
