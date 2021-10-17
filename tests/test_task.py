from task import Task
from meta_task import MetaTask, ElementNotMetaTaskException
from task_factory import TaskFactory
import pytest


def test_task():
    mt = MetaTask("A", 5)
    t = TaskFactory.create_task_from_meta_task(mt)

    assert type(t) == Task
    assert t.get_name() == "A"
    assert t.get_deadline() == 5
    assert t.get_origin() == mt


def test_task_errors():
    with pytest.raises(ElementNotMetaTaskException):
        TaskFactory.create_task_from_meta_task(5)
