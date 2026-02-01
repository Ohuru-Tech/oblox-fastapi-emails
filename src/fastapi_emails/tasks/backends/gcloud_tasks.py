import json
import traceback
from typing import Callable

from google.cloud import tasks_v2

from fastapi_emails.models.task import Task, TaskStatus
from fastapi_emails.repositories.tasks import TasksRepository
from fastapi_emails.tasks.backends.base import TaskSystemBackend


class GCloudTasksBackend(TaskSystemBackend):
    def __init__(self):
        super().__init__()
        self._client = tasks_v2.CloudTasksAsyncClient()
        self._task_registry = {}
        self._tasks_repository = TasksRepository(db=self._db)

    def queue_task(self, task_name: str, task_callable: Callable, **kwargs):
        if not self._task_registry.get(task_name):
            self._task_registry[task_name] = task_callable
        task = self._tasks_repository.create_task(
            task=Task(
                name=task_name, status=TaskStatus.PENDING, task_callable=task_callable
            )
        )
        kwargs["task_id"] = task.id
        kwargs["task_name"] = task_name
        kwargs["secret_key"] = self._settings.task_secret_key
        task = tasks_v2.Task(
            name=self._client.task_path(
                self._settings.gcloud_tasks_project,
                self._settings.gcloud_tasks_location,
                self._settings.gcloud_tasks_queue,
                str(task.id),
            ),
            http_request=tasks_v2.HttpRequest(
                url=f"{self._settings.handler_base}/api/tasks/{task.id}",
                http_method="POST",
                headers={
                    "Content-Type": "application/json",
                    "X-Task-Secret-Key": self._settings.task_secret_key,
                },
                body=json.dumps(kwargs).encode(),
            ),
        )
        return self._client.create_task(
            request=tasks_v2.CreateTaskRequest(
                parent=self._client.queue_path(
                    self._settings.gcloud_tasks_project,
                    self._settings.gcloud_tasks_location,
                    self._settings.gcloud_tasks_queue,
                ),
                task=task,
            )
        )

    def execute_task(self, task_name: str, task_id: int, secret_key: str, **kwargs):
        if secret_key != self._settings.task_secret_key:
            raise ValueError("Invalid secret key")

        task_callable = self._task_registry.get(task_name)
        if not task_callable:
            raise ValueError(f"Task {task_name} not found")

        try:
            result = task_callable(**kwargs)
            self._tasks_repository.update_task_result(task_id=task_id, result=result)
        except Exception as e:
            self._tasks_repository.update_task_result(
                task_id=task_id, error=str(e), traceback=traceback.format_exc()
            )
            raise ValueError(f"Failed to execute task {task_name}: {str(e)}")
