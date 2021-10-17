from scheduler import Scheduler
from scheduler_factory import SchedulerFactory
from task_state import TaskState
import telegram_handler as tg
from task import Task


class Profile:
    def __init__(self, profile_name: str):
        self._profile_name: str = profile_name
        self._scheduler: Scheduler = None
        self._scheduler = (SchedulerFactory.
                           create_scheduler_from_profile_name(profile_name))
        self.registered_user_id: str = None
        self.task_state: TaskState = TaskState.TASK_UNINITED
        self.curr_task: Task = None

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
        self.send_next_task()

    def send_next_task(self):
        if not self.get_scheduler().is_queue_empty():
            tsk = self.get_scheduler().get_next_task()
            tg.TelegramHandler.the().announce_task(self, tsk)
            self.task_state = TaskState.TASK_PENDING
            self.curr_task = tsk
        else:
            msg = ("There are currently no tasks left.")
            tg.TelegramHandler.the().send_msg(self, msg)

    # task reply event functions
    def on_msg_done(self):
        if self.task_state == TaskState.TASK_PENDING:
            self.task_state = TaskState.TASK_DONE
            self.curr_task = None
            if not self.get_scheduler().is_queue_empty():
                msg = ("Task finished. If you like you can get the next " +
                       "task by writing 'next'. If not, the next task will " +
                       "be sent to you tomorrow.")
            else:
                msg = ("Task finished. And what's that...? There are no " +
                       "tasks left! Please enjoy your evening and wait for " +
                       "the next task tomorrow!")
            tg.TelegramHandler.the().send_msg(self, msg)
        else:
            msg = ("You currently do not have an active task.")
            tg.TelegramHandler.the().send_msg(self, msg)

    def on_msg_no(self):
        if self.task_state == TaskState.TASK_PENDING:
            msg = ("Alright then. The task will go right back to where it " +
                   "came from.\nIf you want to redo the task write 'next'. "
                   "Otherwise, the task will come back tomorrow.")
            tg.TelegramHandler.the().send_msg(self, msg)
            self.get_scheduler().insert_queue(0, self.curr_task)
            self.task_state = TaskState.TASK_FAILED
            self.curr_task = None
        else:
            msg = ("You currently have no active task that you can fail.")
            tg.TelegramHandler.the().send_msg(self, msg)

    def on_msg_next(self):
        if (self.task_state == TaskState.TASK_DONE or
                self.task_state == TaskState.TASK_FAILED):
            self.send_next_task()
        else:
            msg = ("Oops! It seems you are not in a state to get a " +
                   "new task! Please finish your current task first.")
            tg.TelegramHandler.the().send_msg(self, msg)
