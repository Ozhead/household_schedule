import pytest
from scheduler import Scheduler, ElementNotMetaTaskException
from meta_task import MetaTask
from task_factory import TaskFactory


def test_scheduler_errors():
    with pytest.raises(ElementNotMetaTaskException):
        Scheduler([5])


def test_scheduler_ctor():
    a = MetaTask("A", 1)
    b = MetaTask("B", 5)
    s = Scheduler([a, b])
    assert s.get_day_ctr() == 0
    assert s.get_tasks() == [a, b]


def test_scheduler_update_schedule():
    a = MetaTask("A", 1)
    b = MetaTask("B", 5)
    c = MetaTask("C", 3)
    s = Scheduler([a, b, c])
    ta = TaskFactory.create_task(a)
    tb = TaskFactory.create_task(b)
    tc = TaskFactory.create_task(c)

    assert s.get_queue() == []
    s.update_queue()
    assert s.get_queue() == [ta, tc, tb]
