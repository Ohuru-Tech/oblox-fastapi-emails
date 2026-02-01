from fastapi_emails.providers.base import BaseEmailProvider
from fastapi_emails.repositories.templates import TemplatesRepository
from fastapi_emails.settings.config import EmailConfigModel
from fastapi_emails.utils.logging import get_logger

logger = get_logger("console_email_provider")


class ConsoleProvider(BaseEmailProvider):
    def __init__(
        self, templates_repository: TemplatesRepository, settings: EmailConfigModel
    ):
        super().__init__(templates_repository, settings)

    async def send_email(self, template_name: str, **kwargs):
        email_content = await self.render_template(template_name, **kwargs)

        # Format email output
        email_output = [
            "=" * 60,
            "EMAIL",
            "=" * 60,
            f"To: {email_content.to}",
            f"Subject: {email_content.subject}",
            "-" * 60,
            email_content.text_content,
        ]

        email_output.append("=" * 60)

        logger.info("\n".join(email_output))
        return True
