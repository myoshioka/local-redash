import sqlfluff
from local_redash.commands.base import Command, ResultData
from local_redash.lib.redash_client import RedashClient


class QueryExportCommand(Command):

    def __init__(self, client: RedashClient) -> None:
        self._redash_client = client

    def execute(self, query_name: str, file_path: str) -> ResultData:
        print(file_path)

        target_query = self._redash_client.search_query(query_name)

        if target_query is None:
            return []

        result = self._save_query(target_query.query, file_path)

        if not result:
            return []

        return [{'query': self.format(target_query.query)}]

    def format(self, query_str: str) -> str:
        return sqlfluff.fix(
            query_str,
            dialect='postgres',
        )

    def _save_query(self, query_str: str, file_path: str) -> bool:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(query_str)
        except IOError:
            return False

        return True
