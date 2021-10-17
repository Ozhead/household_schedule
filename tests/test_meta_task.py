from task_factory import TaskFactory


def test_meta_task_ctor():
    mt = TaskFactory.create_meta_task("Test", 1)
    assert mt.get_name() == "Test"
    assert mt.get_period() == 1
