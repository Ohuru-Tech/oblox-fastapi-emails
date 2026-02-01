from pydantic import BaseModel


class EmailContent(BaseModel):
    to: str
    subject: str
    html_content: str | None = None
    text_content: str
