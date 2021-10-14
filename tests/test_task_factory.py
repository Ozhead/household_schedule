from task_factory import TaskFactory, MissingProperty
import pytest


def test_task_factory_errors():
    with pytest.raises(MissingProperty):
        TaskFactory.create_meta_tasks("tests/name_error.yml")

    with pytest.raises(MissingProperty):
        TaskFactory.create_meta_tasks("tests/period_error.yml")


# check for all printed warnings
def test_task_factory_warnings(capfd):
    warn = ("WARNING: Entry '{'name': 'Test', 'periodicity': 5, 'test': True}'"
            " has more than 2 properties.\n")

    TaskFactory.create_meta_tasks("tests/task_warning.yml")
    out, err = capfd.readouterr()
    print("Captured warning: ")
    print(out)
    assert out == warn


def test_task_factory(capfd):
    mts = TaskFactory.create_meta_tasks("example_tasks.yml")
    out, err = capfd.readouterr()

    assert len(mts) == 2
    assert out == ""    # no warning captured
    assert mts[0].get_name() == "Vacuum living room"
    assert mts[0].get_period() == 5
