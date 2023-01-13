import os
from dotenv import load_dotenv
from os.path import join, dirname
import click
from local_redash.commands.data_source_list import DataSourceListCommand
from local_redash.commands.query import QueryCommand
from local_redash.lib.redash_client import RedashClient

os.environ['NO_PROXY'] = '127.0.0.1,localhost'


@click.command()
@click.option('--query-file', required=True, type=str, help='')
@click.option('--data-source-id', required=True, type=int, help='')
def main(query_file: str, data_source_id: int):

    load_dotenv(join(dirname(__file__), '.env'))

    redash_url = os.environ['REDASH_URL']
    api_key = os.environ['API_KEY']

    client = RedashClient(redash_url, api_key)
    data_source_list_command = DataSourceListCommand(client)
    data_source_list_command.execute()

    query_command = QueryCommand(client, query_file, data_source_id)
    query_command.execute()


if __name__ == '__main__':
    main()
