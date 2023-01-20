from local_redash.commands.base import Command


class CommandExecuter:

    def __init__(self, command: Command):
        self._command = command

    def execute(self) -> None:
        print("execute command")
        self._command.execute()
