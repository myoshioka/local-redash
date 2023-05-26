from typing import TypeAlias, Union

ResultData: TypeAlias = list[dict[str, Union[str, int]]]


class Command:

    def __init__(self) -> None:
        pass

    def execute(self, *args) -> ResultData:
        raise NotImplementedError()

    def filter_columns(self, result_data: ResultData,
                       columns: set[str]) -> ResultData:
        return map(
            lambda x: dict(filter(lambda item: item[0] in columns, x.items())),
            result_data)
