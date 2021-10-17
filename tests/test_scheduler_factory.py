from meta_task import ElementNotMetaTaskListException
from meta_task import ElementNotMetaTaskException
import pytest
from scheduler_factory import SchedulerFactory
from task_factory import TaskFactory


def test_scheduler_factory_errors():
    with pytest.raises(ElementNotMetaTaskListException):
        SchedulerFactory.create_scheduler_from_meta_tasks(5)

    with pytest.raises(ElementNotMetaTaskException):
        SchedulerFactory.create_scheduler_from_meta_tasks([5])


def test_scheduler_factory():
    a = TaskFactory.create_meta_task("A", 5)
    s = SchedulerFactory.create_scheduler_from_meta_tasks(a)
    assert s.get_tasks() == [a]
    mts = TaskFactory.create_meta_tasks_from_yml("profiles/example.yml")
    s = SchedulerFactory.create_scheduler_from_profile_name("example")
    assert s.get_tasks() == mts
