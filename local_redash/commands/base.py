from typing import Union


class Command:
    def __init__(self) -> None:
        pass

    def execute(self, *args) -> list[dict[str, Union[str, int]]]:
        raise NotImplementedError()
