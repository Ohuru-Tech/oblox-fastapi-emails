from functools import lru_cache
from typing import Literal

from pydantic import BaseModel


class EmailConfigModel(BaseModel):
    timezone: str = "Asia/Kolkata"
    provider: Literal["azure", "mailgun", "console"] = "console"

    # Task system settings
    task_system: Literal["taskiq", "google-cloud-tasks"] = "taskiq"
    taskiq_broker: Literal["redis", "memory", "none"] = "none"
    redis_url: str | None = None
    task_secret_key: str | None = None
    gcloud_tasks_project: str | None = None
    gcloud_tasks_location: str | None = None
    gcloud_tasks_queue: str | None = None
    handler_base: str | None = None

    # Mailgun settings
    mailgun_api_key: str | None = None
    mailgun_domain: str | None = None


email_settings: EmailConfigModel | None = None
configured = False


@lru_cache
def get_settings() -> EmailConfigModel:
    global configured
    if not configured:
        raise ValueError(
            "Email settings not configured. Call configure_settings() first."
        )
    return email_settings


def configure_settings(config: EmailConfigModel):
    global email_settings, configured
    configured = True
    email_settings = config
