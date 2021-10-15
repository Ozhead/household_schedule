from meta_task import MetaTask, ElementNotMetaTaskException
from task import Task
from task_factory import TaskFactory
from typing import List


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

    def insert_queue(self, pos: int, t: Task):
        self._queue.insert(pos, t)

    def incr_day_ctr(self):
        self._day_ctr = self._day_ctr + 1

    def update_queue(self):
        # first get a list of tasks that are *not* queued
        # self._queue.append(TaskFactory.create_task(self.get_tasks()[0]))
        scheduled_mts = list(map(lambda x: x.get_origin(), self.get_queue()))

        # create a list of all MetaTasks that do not have a spawn currently
        # in the queue via difference
        # missing_mtasks = list(set(self.get_tasks()) - set(scheduled_mts))
        miss_mtasks = [t for t in self.get_tasks() if t not in scheduled_mts]

        for missing_mtask in miss_mtasks:
            self.schedule_task(missing_mtask)

    def schedule_task(self, mt):
        t = TaskFactory.create_task(mt)

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
