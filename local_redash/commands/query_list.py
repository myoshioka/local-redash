from local_redash.commands.base import Command, ResultData
from local_redash.lib.redash_client import RedashClient


class QueryListCommand(Command):

    def __init__(self, client: RedashClient) -> None:
        self._redash_client = client

    def execute(self) -> ResultData:
        result = self._redash_client.get_query_list()
        keys = set([
            'id',
            'name',
            'created_at',
            'retrieved_at',
            'data_source_id',
            'runtime',
        ])
        return self.filter_columns(result, keys)
