from local_redash.commands.base import Command
from local_redash.lib.redash_client import RedashClient


class QueryListCommand(Command):
    def __init__(self, client: RedashClient) -> None:
        self._redash_client = client

    def execute(self):
        return self._redash_client.get_query_list()
