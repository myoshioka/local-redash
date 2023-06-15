from tabulate import tabulate

from local_redash.commands.base import Command


class CommandExecuter:

    def __init__(self, command: Command, tablefmt: str, stralign: str):
        self._command = command
        self._tablefmt = tablefmt
        self._stralign = stralign

    def execute(
        self,
        *args,
        headers: str = 'keys',
        tablefmt: str | None = None,
        stralign: str | None = None,
    ) -> None:
        tablefmt_val = tablefmt or self._tablefmt
        stralign_val = stralign or self._stralign

        result = self._command.execute(*args)

        print(
            tabulate(result,
                     headers=headers,
                     tablefmt=tablefmt_val,
                     stralign=stralign_val))
