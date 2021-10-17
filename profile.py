from scheduler import Scheduler
from scheduler_factory import SchedulerFactory


class Profile:
    def __init__(self, profile_name: str):
        self._profile_name: str = profile_name
        self._scheduler: Scheduler = None
        self._scheduler = (SchedulerFactory.
                           create_scheduler_from_profile_name(profile_name))
        self.registered_user_id: str = None

    def __str__(self):
        return "Profile: '" + self._profile_name + "'"

    def __repr__(self):
        return self.__str__()

    def get_scheduler(self) -> Scheduler:
        return self._scheduler

    def get_name(self) -> str:
        return self._profile_name

    def is_active(self) -> bool:
        return self.registered_user_id is not None

    def get_user(self):
        return self.registered_user_id

    def set_user(self, usr: str):
        self.registered_user_id = usr
