from typing import Literal

from fastapi_emails.database import get_database_session
from fastapi_emails.repositories.templates import get_templates_repository
from fastapi_emails.services.emails import get_email_service
from fastapi_emails.settings.config import get_settings
from fastapi_emails.tasks.backends.gcloud_tasks import GCloudTasksBackend


def get_task_backend(task_system: Literal["taskiq", "google-cloud-tasks"]):
    task_backends = {"google-cloud-tasks": GCloudTasksBackend}
    return task_backends[task_system]


async def send_email_now(template_name: str, to: str, **kwargs):
    settings = get_settings()
    database_session = await get_database_session()
    templates_repository = get_templates_repository(database_session=database_session)
    email_service = get_email_service(
        settings=settings, templates_repository=templates_repository
    )
    task_backend = get_task_backend(settings.task_system)
    task_backend.queue_task(template_name, email_service.send_email, to=to, **kwargs)
