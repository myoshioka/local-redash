from local_redash.commands.base import Command, ResultData
from local_redash.lib.redash_client import RedashClient


class QueryListCommand(Command):

    def __init__(self, client: RedashClient, columns: list = []) -> None:
        self._redash_client = client
        self._columns = columns

    def execute(self) -> ResultData:
        print(self._columns)

        result = self._redash_client.get_query_list()
        keys = set(self._columns)
        return self.filter_columns(result, keys)
