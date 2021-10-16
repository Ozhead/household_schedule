from meta_task import MetaTask, ElementNotMetaTaskException
from task import Task
from task_factory import TaskFactory
from typing import List


class TaskAlreadyScheduledException(Exception):
    def __init__(self, t):
        self.message = "Task " + str(t) + " is already in the queue."

    def __str__(self):
        return self.message


class Scheduler:
    def __init__(self, meta_tasks: List[MetaTask]):
        for mt in meta_tasks:
            if type(mt) is not MetaTask:
                raise ElementNotMetaTaskException(mt)

        self._tasks: List[MetaTask] = meta_tasks
        self._day_ctr: int = 0
        self._queue: List[Task] = []

    # getter/setter
    def get_tasks(self) -> List[MetaTask]:
        return self._tasks

    def get_day_ctr(self) -> int:
        return self._day_ctr

    def get_queue(self) -> List[Task]:
        return self._queue

    def is_queue_empty(self) -> bool:
        return len(self.get_queue()) == 0

    def get_next_task(self) -> Task:
        if len(self.get_queue()) > 0:
            next_task = self.get_queue()[0]
            del self.get_queue()[0]
            return next_task

        return None

    def insert_queue(self, pos: int, t: Task):
        self._queue.insert(pos, t)

    def advance_day(self):
        # map function is not good for side effects due to lazy evaluation
        # -> good old for loop does the job
        self._day_ctr = self._day_ctr + 1

        for x in self.get_queue():
            x.decr_deadline()

    def update_queue(self):
        # first get a list of tasks that are *not* queued
        # self._queue.append(TaskFactory.create_task(self.get_tasks()[0]))
        scheduled_mts = list(map(lambda x: x.get_origin(), self.get_queue()))

        # create a list of all MetaTasks that do not have a spawn currently
        # in the queue via difference
        # missing_mtasks = list(set(self.get_tasks()) - set(scheduled_mts))
        miss_mtasks = [t for t in self.get_tasks() if t not in scheduled_mts]

        # now filter out all meta tasks that should not be scheduled now
        # more exactly: periodicity matches the current day!
        miss_mtasks = list(filter(lambda x: self.get_day_ctr() % x.get_period() == 0, miss_mtasks))

        for missing_mtask in miss_mtasks:
            self.schedule_task(missing_mtask)

    def schedule_task(self, mt):
        t = TaskFactory.create_task(mt)

        if t in self.get_queue():
            raise TaskAlreadyScheduledException(t)

        pos = 0
        q = self.get_queue()

        for pos in range(len(q)):
            # a higher deadline is encountered -> insert task exactly here
            if q[pos].get_deadline() > t.get_deadline():
                self.insert_queue(pos, t)
                break
        # nothing has been found -> insert at the end
        else:
            self.insert_queue(len(q), t)
