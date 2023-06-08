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
@click.option('--query-file', type=str, help='')
@click.option('--data-source-id', type=int, help='')
@click.pass_context
def query(ctx, query_file, data_source_id):
    ctx.obj.execute(query_file, data_source_id)


@main.command()
@click.pass_context
def data_source_list(ctx):
    ctx.obj.execute()


@main.command()
@click.pass_context
def query_list(ctx):
    ctx.obj.execute()


@main.command()
@click.option('--query-name', type=str, help='')
@click.option('--file-path', type=str, help='')
@click.pass_context
def query_export(ctx, query_name, file_path):
    ctx.obj.execute(query_name, file_path, stralign='left')


if __name__ == '__main__':

    load_dotenv(join(dirname(__file__), '.env'))

    container = Container()
    container.config.redash.url.from_env("REDASH_URL")
    container.config.redash.api_key.from_env("API_KEY")
    container.config.from_yaml(join(dirname(__file__), 'config.yml'))

    container.wire(modules=[__name__])

    main()
