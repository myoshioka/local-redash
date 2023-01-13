class BaseCommand:

    def __init__(self) -> None:
        pass

    def execute(self) -> None:
        raise NotImplementedError()
