from sqlalchemy import String, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models import Base
from app.models.base import SIDMixin, TimestampMixin


class Token(Base, SIDMixin, TimestampMixin):
    __tablename__ = "tokens"

    user_sid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.sid"), nullable=False
    )
    refresh_token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    access_token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
