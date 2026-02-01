from typing import Callable

from fastapi_emails.settings.config import get_settings


class TaskSystemBackend:
    def __init__(self):
        self._settings = get_settings()

    def queue_task(self, task_name: str, task_callable: Callable, **kwargs):
        pass

    def execute_task(self, task_name: str, **kwargs):
        pass

    def get_task_result(self, task_name: str, **kwargs):
        pass

    def get_task_status(self, task_name: str, **kwargs):
        pass
