import os

from local_redash.commands.base import Command, ResultData
from local_redash.lib.redash_client import RedashClient


class RunQueryCommand(Command):

    def __init__(self, client: RedashClient) -> None:
        self._redash_client = client

    def execute(self, query_id: int) -> ResultData:
        result = self._redash_client.query_result(query_id)

        if result is None:
            return []

        return self._sort_columns(result).rows.dict()
