import os
from dotenv import load_dotenv
from os.path import join, dirname
import click
from local_redash.containers import Container
from dependency_injector.wiring import Provide, inject

os.environ['NO_PROXY'] = '127.0.0.1,localhost'


@click.command()
@click.argument('command_name')
@click.option('--query-file', type=str, help='')
@click.option('--data-source-id', type=int, help='')
@inject
def main(command_name: str,
         query_file: str,
         data_source_id: int,
         container: Container = Provide[Container]):

    container.config.command.type.from_value(command_name)

    command_executer = container.executer()
    command_executer.execute()


if __name__ == '__main__':

    load_dotenv(join(dirname(__file__), '.env'))

    container = Container()
    container.config.redash.url.from_env("REDASH_URL")
    container.config.redash.api_key.from_env("API_KEY")
    container.wire(modules=[__name__])

    main()
