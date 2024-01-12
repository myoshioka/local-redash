import os
from os.path import dirname, join

import click
from click_option_group import RequiredMutuallyExclusiveOptionGroup, optgroup
from dependency_injector.wiring import Provide, inject
from dotenv import load_dotenv

from local_redash.containers import Container
from local_redash.lib.config_file import ConfigFile

os.environ['NO_PROXY'] = '127.0.0.1,localhost'


@click.group()
@click.pass_context
@inject
def main(ctx, container: Container = Provide[Container]):
    container.config.command.type.from_value(
        ctx.invoked_subcommand.replace('-', '_'))
    command_executer = container.executer()
    ctx.obj = command_executer


@main.command()
@click.option('--query-file', required=True, type=str, help='')
@click.option('--data-source-id', required=True, type=int, help='')
@click.pass_context
def query(ctx, query_file, data_source_id):
    click.echo('Run query in Sql file.')
    ctx.obj.execute(query_file, data_source_id)


@main.command()
@click.option('--query-id', required=True, type=int, help='')
@click.pass_context
def run_query(ctx, query_id):
    click.echo('Run query.')
    ctx.obj.execute(query_id)


@main.command()
@click.option('--sort-column',
              type=str,
              default='id',
              show_default=True,
              help='')
@click.pass_context
def data_source_list(ctx, sort_column):
    click.echo('List of Data Sources')
    ctx.obj.execute(sort_column)


@main.command()
@click.option('--sort-column',
              type=str,
              default='id',
              show_default=True,
              help='')
@click.pass_context
def query_list(ctx, sort_column):
    click.echo('List of Query')
    ctx.obj.execute(sort_column)


@main.command()
@optgroup.group('Specify query',
                cls=RequiredMutuallyExclusiveOptionGroup,
                help='Specify query to export')
@optgroup.option('--query-name', type=str, help='Query name')
@optgroup.option('--query-id', type=int, help='Query id')
@click.option('--file-path', required=True, type=str, help='')
@click.pass_context
def export_query(ctx, query_name, query_id, file_path):
    click.echo('Export Query')
    query_key: str | int = query_name if query_name else query_id
    ctx.obj.execute(query_key, file_path, stralign='left')


@main.command()
@click.option('--query-id', required=True, type=int, help='')
@click.pass_context
def show_query(ctx, query_id):
    click.echo('Show Query')
    ctx.obj.execute(query_id)


def initialize():
    load_dotenv(join(dirname(__file__), '.env'))

    container = Container()
    # redash-api
    container.config.redash.url.from_env("REDASH_URL")
    container.config.redash.api_key.from_env("API_KEY")
    # config
    config_file = ConfigFile()
    container.config.from_yaml(config_file.file_path())

    container.wire(modules=[__name__])

    main()


if __name__ == '__main__':
    initialize()
