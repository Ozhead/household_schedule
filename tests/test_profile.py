from task_factory import TaskFactory
from profile import Profile


def test_profile():
    mts = TaskFactory.create_meta_tasks_from_yml("profiles/example.yml")
    pr = Profile("example")

    assert pr.get_scheduler().get_tasks() == mts
    assert pr.get_name() == "example"
