from local_redash.commands.base import BaseCommand
from local_redash.lib.redash_client import RedashClient
from tabulate import tabulate


class DataSourceListCommand(BaseCommand):

    def __init__(self, redash_client: RedashClient) -> None:
        self._redash_client = redash_client

    def execute(self) -> None:
        result = self._redash_client.get_data_source_list()
        print(
            tabulate(result,
                     headers="keys",
                     tablefmt="psql",
                     stralign='center'))
