import pytest
from scheduler import Scheduler, ElementNotMetaTaskException
from meta_task import MetaTask


def test_scheduler_errors():
    with pytest.raises(ElementNotMetaTaskException):
        Scheduler([5])


def test_scheduler_ctor():
    a = MetaTask("A", 1)
    b = MetaTask("B", 5)
    s = Scheduler([a, b])
    assert s.get_day_ctr() == 0
    assert s.get_tasks() == [a, b]
