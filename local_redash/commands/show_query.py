from local_redash.commands.base import Command, ResultData
from local_redash.lib.redash_client import RedashClient


class ShowQueryCommand(Command):

    def __init__(self, client: RedashClient) -> None:
        self._redash_client = client

    def execute(self, query_id: int) -> ResultData:
        query = self._redash_client.get_query(query_id)
        data_source = self._redash_client.get_data_source(query.data_source_id)

        formatted_query = self.format_query(query.query, data_source.type)

        return [{'query': formatted_query}]
