from meta_task import MetaTask, ElementNotMetaTaskException


class ElementNotTaskException(Exception):
    def __init__(self, elem):
        self.message = "Element " + str(elem) + " is not of type Task"

    def __str__(self):
        return self.message


class Task:
    def __init__(self, mt: MetaTask):
        if type(mt) != MetaTask:
            raise ElementNotMetaTaskException(mt)

        self._name: str = mt.get_name()
        self._deadline: int = mt.get_period()
        self._origin: MetaTask = mt

    def __str__(self):
        return "<'" + self.get_name() + "', " + str(self.get_deadline()) + ">"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if type(other) is not Task:
            raise ElementNotTaskException(other)

        return self.get_origin() == other.get_origin()

    # setter/getter
    def get_name(self) -> str:
        return self._name

    def get_deadline(self) -> int:
        return self._deadline

    def get_origin(self) -> MetaTask:
        return self._origin

    def decr_deadline(self):
        self._deadline = self._deadline - 1
