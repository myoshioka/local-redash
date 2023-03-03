from local_redash.commands.base import Command, ResultData
from local_redash.lib.redash_client import RedashClient


class DataSourceListCommand(Command):

    def __init__(self, client: RedashClient) -> None:
        self._redash_client = client

    def execute(self) -> ResultData:
        return self._redash_client.get_data_source_list()
