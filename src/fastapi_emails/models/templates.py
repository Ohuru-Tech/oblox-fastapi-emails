from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_emails.models.base import Base


class Template(Base):
    __tablename__ = "templates"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    html_content: Mapped[str] = mapped_column(Text, nullable=True)
    text_content: Mapped[str] = mapped_column(Text, nullable=False)
