import pytest
from scheduler import TaskAlreadyScheduledException
from meta_task import ElementNotMetaTaskException
from task_factory import TaskFactory
from scheduler_factory import SchedulerFactory


def test_scheduler_errors():
    with pytest.raises(ElementNotMetaTaskException):
        SchedulerFactory.create_scheduler_from_meta_tasks([5])

    a = TaskFactory.create_meta_task("A", 1)
    s = SchedulerFactory.create_scheduler_from_meta_tasks([a])
    s.schedule_task(a)

    with pytest.raises(TaskAlreadyScheduledException):
        s.schedule_task(a)


def test_scheduler_ctor():
    a = TaskFactory.create_meta_task("A", 1)
    b = TaskFactory.create_meta_task("B", 5)
    s = SchedulerFactory.create_scheduler_from_meta_tasks([a, b])
    assert s.get_day_ctr() == 0
    assert s.get_tasks() == [a, b]


# basic, manual task scheduling
def test_scheduler_schedule_task():
    a = TaskFactory.create_meta_task("A", 1)
    b = TaskFactory.create_meta_task("B", 5)
    c = TaskFactory.create_meta_task("C", 3)
    d = TaskFactory.create_meta_task("D", 3)
    s = SchedulerFactory.create_scheduler_from_meta_tasks([a, b, c, d])
    ta = TaskFactory.create_task_from_meta_task(a)
    tb = TaskFactory.create_task_from_meta_task(b)
    tc = TaskFactory.create_task_from_meta_task(c)
    td = TaskFactory.create_task_from_meta_task(d)

    s.schedule_task(a)
    assert s.get_queue() == [ta]
    s.schedule_task(b)
    assert s.get_queue() == [ta, tb]
    s.schedule_task(c)
    assert s.get_queue() == [ta, tc, tb]
    s.schedule_task(d)
    assert s.get_queue() == [ta, tc, td, tb]


# basic checking that all missing tasks are scheduled
def test_scheduler_update_schedule():
    a = TaskFactory.create_meta_task("A", 1)
    b = TaskFactory.create_meta_task("B", 5)
    c = TaskFactory.create_meta_task("C", 3)
    s = SchedulerFactory.create_scheduler_from_meta_tasks([a, b, c])
    ta = TaskFactory.create_task_from_meta_task(a)
    tb = TaskFactory.create_task_from_meta_task(b)
    tc = TaskFactory.create_task_from_meta_task(c)

    # empty queue
    assert s.get_queue() == []
    s.update_queue()
    assert s.get_queue() == [ta, tc, tb]

    # not empty queue
    s._queue = [tb]
    s.update_queue()
    assert s.get_queue() == [ta, tc, tb]

    # full queue
    s._queue = [ta, tc, tb]
    s.update_queue()
    assert s.get_queue() == [ta, tc, tb]


# check if all tasks' deadlines are decreasing
def test_scheduler_advance_day():
    a = TaskFactory.create_meta_task("A", 2)
    b = TaskFactory.create_meta_task("B", 3)
    s = SchedulerFactory.create_scheduler_from_meta_tasks([a, b])
    s.update_queue()

    assert s.get_day_ctr() == 0
    s.advance_day()
    assert s.get_day_ctr() == 1
    assert s.get_queue()[0].get_deadline() == 1
    assert s.get_queue()[1].get_deadline() == 2


# check if popping tasks from the queue works
def test_scheduler_next_task():
    a = TaskFactory.create_meta_task("A", 5)
    b = TaskFactory.create_meta_task("B", 1)
    s = SchedulerFactory.create_scheduler_from_meta_tasks([a, b])
    ta = TaskFactory.create_task_from_meta_task(a)
    tb = TaskFactory.create_task_from_meta_task(b)

    assert s.is_queue_empty() is True
    s.update_queue()
    assert s.is_queue_empty() is False
    assert s.get_next_task() == tb
    assert s.get_next_task() == ta
    assert s.is_queue_empty() is True


# check that tasks are not re-scheduled again if the time has not
# advanced enough for the task to reappear
def test_scheduler_periodic_scheduling():
    a = TaskFactory.create_meta_task("A", 5)
    b = TaskFactory.create_meta_task("B", 3)
    s = SchedulerFactory.create_scheduler_from_meta_tasks([a, b])
    ta = TaskFactory.create_task_from_meta_task(a)
    tb = TaskFactory.create_task_from_meta_task(b)

    s.update_queue()
    assert s.get_queue() == [tb, ta]

    t = s.get_next_task()
    s.advance_day()
    assert t == tb
    assert s.get_queue() == [ta]
    # only 1 day advanced -> task B must not be scheduled again!
    s.update_queue()
    assert s.get_queue() == [ta]
    # day 2 -> ta is popped, nothing scheduled
    t = s.get_next_task()
    s.advance_day()
    assert t == ta
    assert s.get_queue() == []
    s.update_queue()
    assert s.get_queue() == []
    # day 3 -> nothing popped, tb is scheduled
    t = s.get_next_task()
    s.advance_day()
    assert t is None
    assert s.get_queue() == []
    s.update_queue()
    assert s.get_queue() == [tb]
