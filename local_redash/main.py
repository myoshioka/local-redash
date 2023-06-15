import os
from os.path import dirname, join

import click
from dependency_injector.wiring import Provide, inject
from dotenv import load_dotenv

from local_redash.containers import Container

os.environ['NO_PROXY'] = '127.0.0.1,localhost'


@click.group()
@click.pass_context
@inject
def main(ctx, container: Container = Provide[Container]):
    click.echo(f'call {ctx.invoked_subcommand}')

    container.config.command.type.from_value(
        ctx.invoked_subcommand.replace('-', '_'))
    command_executer = container.executer()
    ctx.obj = command_executer


@main.command()
@click.option('--query-file', required=True, type=str, help='')
@click.option('--data-source-id', required=True, type=int, help='')
@click.pass_context
def query(ctx, query_file, data_source_id):
    ctx.obj.execute(query_file, data_source_id)


@main.command()
@click.option('--sort-column',
              type=str,
              default='id',
              show_default=True,
              help='')
@click.pass_context
def data_source_list(ctx, sort_column):
    ctx.obj.execute(sort_column)


@main.command()
@click.option('--sort-column',
              type=str,
              default='id',
              show_default=True,
              help='')
@click.pass_context
def query_list(ctx, sort_column):
    ctx.obj.execute(sort_column)


@main.command()
@click.option('--query-name', required=True, type=str, help='')
@click.option('--file-path', required=True, type=str, help='')
@click.pass_context
def export_query(ctx, query_name, file_path):
    ctx.obj.execute(query_name, file_path, stralign='left')


@main.command()
@click.option('--query-id', required=True, type=int, help='')
@click.pass_context
def show_query(ctx, query_id):
    ctx.obj.execute(query_id)


if __name__ == '__main__':

    load_dotenv(join(dirname(__file__), '.env'))

    container = Container()
    # redash-api
    container.config.redash.url.from_env("REDASH_URL")
    container.config.redash.api_key.from_env("API_KEY")
    # config
    container.config.from_yaml(join(dirname(__file__), 'config.yml'))

    container.wire(modules=[__name__])

    main()
