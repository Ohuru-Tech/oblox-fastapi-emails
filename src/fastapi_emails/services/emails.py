from typing import Literal

from fastapi import Depends

from fastapi_emails.providers.base import BaseEmailProvider
from fastapi_emails.providers.console import ConsoleProvider
from fastapi_emails.providers.mailgun import MailgunProvider
from fastapi_emails.repositories.templates import (
    TemplatesRepository,
    get_templates_repository,
)
from fastapi_emails.settings.config import EmailConfigModel, get_settings


def get_email_provider(
    provider: Literal["azure", "mailgun", "console"],
) -> BaseEmailProvider:
    providers = {"console": ConsoleProvider, "mailgun": MailgunProvider}
    return providers[provider]


class EmailService:
    def __init__(
        self, settings: EmailConfigModel, templates_repository: TemplatesRepository
    ):
        self._settings = settings
        self._templates_repository = templates_repository
        self._provider = get_email_provider(settings.provider)(
            templates_repository, settings
        )

    async def send_email(self, template_name: str, to: str, **kwargs):
        await self._provider.send_email(template_name, to=to, **kwargs)


def get_email_service(
    settings: EmailConfigModel = Depends(get_settings),
    templates_repository: TemplatesRepository = Depends(get_templates_repository),
) -> EmailService:
    return EmailService(settings, templates_repository)
