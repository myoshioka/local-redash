from local_redash.commands.base import Command


class CommandExecuter:

    def __init__(self, command: Command):
        self._command = command

    def execute(self) -> None:
        print(f'execute command: {self._command.__class__.__name__}')
        self._command.execute()
