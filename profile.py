from scheduler import Scheduler
from scheduler_factory import SchedulerFactory
from task_state import TaskState
import telegram_handler as tg


class Profile:
    def __init__(self, profile_name: str):
        self._profile_name: str = profile_name
        self._scheduler: Scheduler = None
        self._scheduler = (SchedulerFactory.
                           create_scheduler_from_profile_name(profile_name))
        self.registered_user_id: str = None
        self.task_state: TaskState = TaskState.TASK_UNINITED

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

    def get_task_state(self) -> TaskState:
        return self.task_state

    def set_task_state(self, state: TaskState):
        self.task_state = state

    def logon(self, usr):
        self.set_user(usr)

    def logoff(self):
        self.set_user(None)

    # aka main method
    def update(self):
        self.get_scheduler().update_queue()
        tsk = self.get_scheduler().get_next_task()
        print(tsk)
        tg.TelegramHandler.the().announce_task(self, tsk)
        self.task_state = TaskState.TASK_PENDING
