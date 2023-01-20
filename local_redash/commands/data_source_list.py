from local_redash.commands.base import Command
from local_redash.lib.redash_client import RedashClient
from tabulate import tabulate


class DataSourceListCommand(Command):

    def __init__(self, client: RedashClient) -> None:
        self._redash_client = client

    def execute(self) -> None:
        result = self._redash_client.get_data_source_list()
        print(
            tabulate(result,
                     headers="keys",
                     tablefmt="psql",
                     stralign='center'))
