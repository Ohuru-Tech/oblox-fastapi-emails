from enum import Enum

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_emails.models.base import Base


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(Base):
    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        SQLAlchemyEnum(TaskStatus), nullable=False
    )
    result: Mapped[str] = mapped_column(Text, nullable=True)
    error: Mapped[str] = mapped_column(Text, nullable=True)
    traceback: Mapped[str] = mapped_column(Text, nullable=True)
