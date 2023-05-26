import os

from local_redash.commands.base import Command, ResultData
from local_redash.lib.redash_client import RedashClient


class QueryCommand(Command):

    def __init__(self, client: RedashClient) -> None:
        self._redash_client = client

    def execute(self, query_path: str, data_source_id: str) -> ResultData:
        query_str = self.__get_query(query_path)
        query_name = self.__get_file_name(query_path)

        target_query = self._redash_client.search_query(query_name)

        if target_query is None:
            created_query = self._redash_client.create_query(
                data_source_id, query_name, query_str)
            result = self._redash_client.query_result(created_query.id)

        else:
            self._redash_client.update_query(target_query.id, query_str)
            result = self._redash_client.query_result(target_query.id)

        return result.rows.dict()

    def __get_query(self, query_file_path: str) -> str:
        with open(query_file_path, 'r', encoding='utf-8') as f:
            query = f.read()
        return query

    def __get_file_name(self, file_path: str) -> str:
        return os.path.basename(file_path).split('.')[0]
