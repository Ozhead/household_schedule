from enum import Enum


class TaskState(Enum):
    TASK_UNINITED = 0
    TASK_PENDING = 1
    TASK_DONE = 2
    TASK_FAILED = 3
