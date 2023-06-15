import os

import sqlfluff
from local_redash.commands.base import Command, ResultData
from local_redash.lib.redash_client import RedashClient
from local_redash.models.redash_client import DataSourceType, SqlFormatDialects


class ExportQueryCommand(Command):

    def __init__(self, client: RedashClient) -> None:
        self._redash_client = client

    def execute(self, query_name: str, file_path: str) -> ResultData:
        if not os.path.isdir(file_path):
            return []
        file_path = file_path.rstrip(os.path.sep)

        target_query = self._redash_client.search_query(query_name)

        if target_query is None:
            return []

        data_source = self._redash_client.get_data_source(
            target_query.data_source_id)

        formatted_query = self.format(target_query.query, data_source.type)
        result = self._save_query(formatted_query,
                                  f'{file_path}/{query_name}.sql')

        if not result:
            return []

        return [{'exported-query': formatted_query}]

    def format(self, query_str: str, data_source_type: DataSourceType) -> str:
        dialect = SqlFormatDialects.from_datasource_type(data_source_type)

        return sqlfluff.fix(
            query_str,
            dialect=dialect,
        )

    def _save_query(self, query_str: str, file_path: str) -> bool:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(query_str)
        except IOError:
            return False

        return True
