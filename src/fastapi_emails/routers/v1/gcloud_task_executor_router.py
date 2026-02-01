"""
GCloud Task Executor Router

This is a plug and play api system to be registered with your FastAPI application to handle GCloud Tasks requests.

Here is how it works:
- The GCloud task backend will queue tasks using the tasks api,
- The task api will be called by GCloud Tasks when the task is ready to be executed,
- The task api will execute the task and store the results in the database
"""

from fastapi import APIRouter

from fastapi_emails.schemas.tasks import TaskExecutionRequest
from fastapi_emails.tasks.backends.gcloud_tasks import GCloudTasksBackend

gcloud_task_executor_router = APIRouter(prefix="/api/gcloud/tasks", tags=["tasks"])


@gcloud_task_executor_router.post("/")
async def execute_gcloud_task(task_execution_request: TaskExecutionRequest):
    task_backend = GCloudTasksBackend()
    task_backend.execute_task(
        task_name=task_execution_request.task_name,
        task_id=task_execution_request.task_id,
        secret_key=task_execution_request.secret_key,
        **task_execution_request.model_dump(exclude={'task_name', 'task_id', 'secret_key'}),
    )
