from meta_task import MetaTask
from typing import List


class ElementNotMetaTaskException(Exception):
    def __init__(self, elem):
        self.message = "Element " + str(elem) + " is not of type MetaTask"

    def __str__(self):
        return self.message


# MetaTaskList = NewType('MetaTaskList', list(MetaTask))


class Scheduler:
    def __init__(self, meta_tasks: List[MetaTask]):
        for mt in meta_tasks:
            if type(mt) is not MetaTask:
                raise ElementNotMetaTaskException(mt)

        self._tasks: List[MetaTask] = meta_tasks
        self._day_ctr: int = 0
        self._queue = []

    # getter/setter
    def get_tasks(self) -> List[MetaTask]:
        return self._tasks

    def get_day_ctr(self) -> int:
        return self._day_ctr

    def incr_day_ctr(self):
        self._day_ctr = self._day_ctr + 1
