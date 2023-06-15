from local_redash.commands.base import Command, ResultData
from local_redash.lib.redash_client import RedashClient


class QueryListCommand(Command):

    def __init__(self, client: RedashClient, columns: list = []) -> None:
        self._redash_client = client
        self._columns = columns

    def execute(self, sort_column: str | None = None) -> ResultData:
        query_list = self._redash_client.get_query_list()
        keys = set(self._columns)
        filtered_query_list = self.filter_columns(query_list.dict(), keys)

        if sort_column is None:
            return filtered_query_list

        return self.sort_records(filtered_query_list, sort_column)
