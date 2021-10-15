from meta_task import MetaTask, ElementNotMetaTaskException


class Task:
    def __init__(self, mt: MetaTask):
        if type(mt) != MetaTask:
            raise ElementNotMetaTaskException(mt)

        self._name: str = mt.get_name()
        self._deadline: int = mt.get_period()
        self._origin: MetaTask = mt

    # setter/getter
    def get_name(self) -> str:
        return self._name

    def get_deadline(self) -> int:
        return self._deadline

    def get_origin(self) -> MetaTask:
        return self._origin

    def decr_deadline(self):
        self._deadline = self._deadline - 1
