from meta_task import MetaTask, ElementNotMetaTaskException
from meta_task import ElementNotMetaTaskListException
from scheduler import Scheduler
from typing import List
from task_factory import TaskFactory


class SchedulerFactory:
    @staticmethod
    def create_scheduler_from_meta_tasks(mts: List[MetaTask]) -> Scheduler:
        # check for MetaTasks
        if type(mts) != list and type(mts) != MetaTask:
            raise ElementNotMetaTaskListException(mts)

        # singular MetaTask -> convert it to a list to be iteratable
        if type(mts) != list and type(mts) == MetaTask:
            mts = [mts]

        for mt in mts:
            if type(mt) != MetaTask:
                raise ElementNotMetaTaskException(mt)

        return Scheduler(mts)

    @staticmethod
    def create_scheduler_from_profile_name(name: str) -> Scheduler:
        mts = TaskFactory.create_meta_tasks_from_yml("profiles/" + name +
                                                     ".yml")
        return Scheduler(mts)
