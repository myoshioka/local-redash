import os
from local_redash.commands.base import Command
from local_redash.lib.redash_client import RedashClient
from tabulate import tabulate


class QueryCommand(Command):

    def __init__(self, client: RedashClient, query_path: str,
                 data_source_id: str) -> None:
        self._redash_client = client
        self._query_path = query_path
        self._data_source_id = data_source_id

    def execute(self) -> None:
        query_str = self.__get_query(self._query_path)
        query_name = self.__get_file_name(self._query_path)

        target_query = self._redash_client.search_query(query_name)

        if target_query is None:
            created_query = self._redash_client.create_query(
                self._data_source_id, query_name, query_str)
            result = self._redash_client.get_fresh_query_result(
                created_query['id'])

        else:
            self._redash_client.update_query(target_query['id'], query_str)
            result = self._redash_client.get_fresh_query_result(
                target_query['id'])

        print(
            tabulate(result,
                     headers="keys",
                     tablefmt="psql",
                     stralign='center'))

    def __get_query(self, query_file_path: str) -> str:
        with open(query_file_path, 'r', encoding='utf-8') as f:
            query = f.read()
        return query

    def __get_file_name(self, file_path: str) -> str:
        return os.path.basename(file_path).split('.')[0]
