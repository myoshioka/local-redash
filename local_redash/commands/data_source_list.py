from local_redash.commands.base import Command, ResultData
from local_redash.lib.redash_client import RedashClient


class DataSourceListCommand(Command):

    def __init__(self, client: RedashClient) -> None:
        self._redash_client = client

    def execute(self, sort_column: str | None = None) -> ResultData:
        data_source_list = self._redash_client.get_data_source_list()

        if sort_column is None:
            return data_source_list.dict()

        return self.sort_records(data_source_list.dict(), sort_column)
