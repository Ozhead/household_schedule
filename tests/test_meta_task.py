from meta_task import MetaTask


def test_meta_task_ctor():
    mt = MetaTask("Test", 1)
    assert mt.get_name() == "Test"
    assert mt.get_period() == 1
