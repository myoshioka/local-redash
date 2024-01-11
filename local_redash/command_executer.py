import json

from tabulate import tabulate

from local_redash.commands.base import Command, ResultDataRow


class CommandExecuter:

    def __init__(self, command: Command, tablefmt: str, stralign: str,
                 maxcolwidths: int):
        self._command = command
        self._tablefmt = tablefmt
        self._stralign = stralign
        self._maxcolwidths = maxcolwidths

    def execute(
        self,
        *args,
        headers: str = 'keys',
        tablefmt: str | None = None,
        stralign: str | None = None,
        maxcolwidths: int | None = None,
    ) -> None:
        tablefmt_val = tablefmt or self._tablefmt
        stralign_val = stralign or self._stralign
        maxcolwidths_val = maxcolwidths or self._maxcolwidths

        result = self._command.execute(*args)
        converted_result = list(
            map(lambda row: self.convert_values_to_string(row), result))

        if len(converted_result) == 0:
            print('Data does not exist.')
            return

        print(
            tabulate(
                converted_result,
                headers=headers,
                tablefmt=tablefmt_val,
                stralign=stralign_val,
                maxcolwidths=maxcolwidths_val,
            ))

    def convert_values_to_string(self, row: ResultDataRow) -> ResultDataRow:
        for key, value in row.items():
            if isinstance(value, dict):
                row[key] = json.dumps(value, ensure_ascii=False)
            else:
                row[key] = str(value)
        return row
