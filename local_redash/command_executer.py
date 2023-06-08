from tabulate import tabulate

from local_redash.commands.base import Command


class CommandExecuter:

    def __init__(self, command: Command):
        self._command = command

    def execute(
        self,
        *args,
        headers: str = 'keys',
        tablefmt: str = 'psql',
        stralign: str = 'center',
    ) -> None:
        result = self._command.execute(*args)
        print(
            tabulate(result,
                     headers=headers,
                     tablefmt=tablefmt,
                     stralign=stralign))
