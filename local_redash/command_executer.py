from local_redash.commands.base import Command
from tabulate import tabulate


class CommandExecuter:

    def __init__(self, command: Command):
        self._command = command

    def execute(self, *args) -> None:
        result = self._command.execute(*args)
        print(
            tabulate(result,
                     headers="keys",
                     tablefmt="psql",
                     stralign='center'))
