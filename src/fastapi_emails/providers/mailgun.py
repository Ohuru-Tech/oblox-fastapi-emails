import httpx

from fastapi_emails.providers.base import BaseEmailProvider
from fastapi_emails.repositories.templates import TemplatesRepository
from fastapi_emails.settings.config import EmailConfigModel


class MailgunProvider(BaseEmailProvider):
    def __init__(
        self, templates_repository: TemplatesRepository, settings: EmailConfigModel
    ):
        super().__init__(templates_repository, settings)
        self._mailgun_api_key = settings.mailgun_api_key
        self._mailgun_domain = settings.mailgun_domain

        if not self._mailgun_api_key or not self._mailgun_domain:
            raise ValueError("Mailgun API key and domain are required")

    async def send_email(self, template_name: str, **kwargs):
        email_content = await self.render_template(template_name, **kwargs)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.mailgun.net/v3/{self._mailgun_domain}/messages",
                auth=(("api", self._mailgun_api_key)),
                headers={"Content-Type": "multipart/form-data"},
                data={
                    "from": f"Mind Demystified <DoNotReply@{self._mailgun_domain}>",
                    "to": email_content.to,
                    "subject": email_content.subject,
                    "html": email_content.html_content,
                    "text": email_content.text_content,
                },
            )

            if response.status_code != 200:
                raise Exception(f"Failed to send email: {response.text}")

        return True
