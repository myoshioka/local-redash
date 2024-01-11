import os

from local_redash.commands.base import Command, ResultData
from local_redash.lib.redash_client import RedashClient
from local_redash.models.redash_client import QueryDetail


class ExportQueryCommand(Command):

    def __init__(self, client: RedashClient) -> None:
        self._redash_client = client

    def execute(self, query_key: str | int, file_path: str) -> ResultData:
        if not os.path.isdir(file_path):
            return []
        file_path = file_path.rstrip(os.path.sep)

        target_query: QueryDetail | None = None

        if type(query_key) == str:
            target_query = self.from_query_name(query_key)
        elif type(query_key) == int:
            target_query = self.from_query_id(query_key)
        else:
            pass

        if target_query is None:
            return []

        data_source = self._redash_client.get_data_source(
            target_query.data_source_id)

        formatted_query = self.format_query(target_query.query,
                                            data_source.type)
        result = self._save_query(formatted_query,
                                  f'{file_path}/{target_query.name}.sql')

        if not result:
            return []

        return [{'exported-query': formatted_query}]

    def from_query_id(self, query_id: int) -> QueryDetail | None:
        return self._redash_client.get_query(query_id)

    def from_query_name(self, query_name: str) -> QueryDetail | None:
        query = self._redash_client.search_query(query_name)

        if query is None:
            return None

        return self._redash_client.get_query(query.id)

    def _save_query(self, query_str: str, file_path: str) -> bool:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(query_str)
        except IOError:
            return False

        return True
