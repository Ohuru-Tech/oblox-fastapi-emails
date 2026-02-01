from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi_emails.settings.config import get_settings
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

settings = get_settings()


def get_current_time():
    return datetime.now(tz=ZoneInfo(settings.timezone))


class Base:
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=get_current_time,
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=get_current_time,
        onupdate=get_current_time,
    )
