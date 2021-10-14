class MetaTask:
    REQUIRED_PROPERTIES: list = ["name", "periodicity"]

    def __init__(self, name: str, periodicity: int):
        # constants
        self._name = name
        self._periodicity = periodicity

    # getter methods
    def get_name(self) -> str:
        return self._name

    def get_period(self) -> int:
        return self._periodicity
