from dependency_injector import containers, providers
from local_redash.lib.redash_client import RedashClient
from local_redash.commands.data_source_list import DataSourceListCommand
from local_redash.commands.query import QueryCommand
from local_redash.command_executer import CommandExecuter


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    redash_client = providers.Factory(
        RedashClient,
        redash_url=config.redash.url,
        api_key=config.redash.api_key,
    )

    data_source_list_command = providers.Singleton(
        DataSourceListCommand,
        client=redash_client,
    )

    query_command = providers.Singleton(
        QueryCommand,
        client=redash_client,
        # query_file=config.command.query.query_file,
        # data_source_id=config.command.query.data_source_id,
        query_path="./queries/query_test.sql",
        data_source_id="1",
    )

    command = providers.Selector(
        config.command.type,
        data_source_list=data_source_list_command,
        query=query_command,
    )

    executer = providers.Factory(
        CommandExecuter,
        command=command,
    )
