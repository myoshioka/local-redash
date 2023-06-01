from typing import Callable, TypeAlias, Union

ResultData: TypeAlias = list[dict[str, Union[str, int]]]


class Command:

    def __init__(self) -> None:
        pass

    def execute(self, *args) -> ResultData:
        raise NotImplementedError()

    def filter_columns(self, result_data: ResultData,
                       columns: set[str]) -> ResultData:

        check: Callable[[tuple[str, str | int]],
                        bool] = lambda item: item[0] in columns
        return list(map(lambda x: dict(filter(check, x.items())), result_data))
