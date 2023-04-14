from os.path import join, dirname
from dependency_injector import containers, providers
from redash_toolbelt import Redash
from local_redash.lib.redash_client import RedashClient
from local_redash.command_executer import CommandExecuter
from local_redash.commands.data_source_list import DataSourceListCommand
from local_redash.commands.query import QueryCommand
from local_redash.commands.query_list import QueryListCommand


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    redash = providers.Factory(
        Redash,
        redash_url=config.redash.url,
        api_key=config.redash.api_key,
    )

    redash_client = providers.Factory(RedashClient, redash=redash)

    data_source_list_command = providers.Singleton(
        DataSourceListCommand,
        client=redash_client,
    )

    query_command = providers.Singleton(
        QueryCommand,
        client=redash_client,
    )

    query_list_command = providers.Singleton(QueryListCommand,
                                             client=redash_client,
                                             columns=config.columns.query_list)

    command = providers.Selector(config.command.type,
                                 data_source_list=data_source_list_command,
                                 query=query_command,
                                 query_list=query_list_command)

    executer = providers.Factory(
        CommandExecuter,
        command=command,
    )
