class ElementNotMetaTaskException(Exception):
    def __init__(self, elem):
        self.message = "Element " + str(elem) + " is not of type MetaTask."

    def __str__(self):
        return self.message


class ElementNotMetaTaskListException(Exception):
    def __init__(self, elem):
        self.message = ("Element " + str(elem) + 
                        " is not of type List[MetaTask].")

    def __str__(self):
        return self.message


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

    def __eq__(self, other):
        if type(other) is not MetaTask:
            raise ElementNotMetaTaskException(other)

        return (self.get_name() == other.get_name() and
                self.get_period() == other.get_period())

    # getter methods
    def get_name(self) -> str:
        return self._name

    def get_period(self) -> int:
        return self._periodicity
