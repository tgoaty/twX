import uuid
from .base import Base
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    sid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    is_activated = Column(Boolean, nullable=False, default=False)
    activation_link = Column(
        String,
    )
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_active = Column(DateTime, default=datetime.now(timezone.utc))
