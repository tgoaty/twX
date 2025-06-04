import uuid
from .base import Base
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.now())
    last_active = Column(DateTime, default=datetime.now())
