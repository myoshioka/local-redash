from dependency_injector import containers, providers

from local_redash.command_executer import CommandExecuter
from local_redash.commands.data_source_list import DataSourceListCommand
from local_redash.commands.export_query import ExportQueryCommand
from local_redash.commands.query import QueryCommand
from local_redash.commands.query_list import QueryListCommand
from local_redash.commands.run_query import RunQueryCommand
from local_redash.commands.show_query import ShowQueryCommand
from local_redash.lib.redash_client import RedashClient


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    redash_client = providers.Factory(
        RedashClient,
        redash_url=config.redash.url,
        api_key=config.redash.api_key,
    )

    # Commands
    data_source_list_command = providers.Singleton(
        DataSourceListCommand,
        client=redash_client,
    )

    query_command = providers.Singleton(
        QueryCommand,
        client=redash_client,
    )

    run_query_command = providers.Singleton(
        RunQueryCommand,
        client=redash_client,
    )

    query_list_command = providers.Singleton(QueryListCommand,
                                             client=redash_client,
                                             columns=config.columns.query_list)

    export_query_command = providers.Singleton(
        ExportQueryCommand,
        client=redash_client,
    )

    show_query_command = providers.Singleton(
        ShowQueryCommand,
        client=redash_client,
    )

    # Command to execute
    command = providers.Selector(
        config.command.type,
        data_source_list=data_source_list_command,
        query=query_command,
        query_list=query_list_command,
        export_query=export_query_command,
        show_query=show_query_command,
        run_query=run_query_command,
    )

    executer = providers.Factory(
        CommandExecuter,
        command=command,
        tablefmt=config.table_format.tablefmt,
        stralign=config.table_format.stralign,
        maxcolwidths=config.table_format.maxcolwidths,
    )
