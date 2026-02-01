from jinja2 import Environment

from fastapi_emails.repositories.templates import TemplatesRepository
from fastapi_emails.schemas.emails import EmailContent
from fastapi_emails.settings.config import EmailConfigModel


class BaseEmailProvider:
    def __init__(
        self, templates_repository: TemplatesRepository, settings: EmailConfigModel
    ):
        self._templates_repository = templates_repository

    async def render_template(self, template_name: str, **kwargs) -> EmailContent:
        template = await self._templates_repository.get_template_by_name(template_name)
        jinja_html_template = Environment().from_string(source=template.html_content)
        jinja_text_template = Environment().from_string(source=template.text_content)
        html_content = jinja_html_template.render(**kwargs)
        text_content = jinja_text_template.render(**kwargs)

        return EmailContent(
            to=kwargs.get("to"),
            subject=template.subject,
            html_content=html_content,
            text_content=text_content,
        )

    def send_email(self, template_name: str, **kwargs):
        pass
