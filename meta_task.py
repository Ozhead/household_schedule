class MetaTask:
    REQUIRED_PROPERTIES: list = ["name", "periodicity"]

    def __init__(self, name: str, periodicity: int):
        # constants
        self._name = name
        self._periodicity = periodicity

    def __str__(self):
        return "<'" + self.get_name() + "', " + str(self.get_period()) + ">"

    def __repr__(self):
        return self.__str__()

    # getter methods
    def get_name(self) -> str:
        return self._name

    def get_period(self) -> int:
        return self._periodicity
