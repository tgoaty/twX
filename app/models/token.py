import uuid
from sqlalchemy import Column, String, ForeignKey, UUID
from app.models import Base


class Token(Base):
    __tablename__ = "tokens"

    sid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user = Column(UUID(as_uuid=True), ForeignKey("users.sid"), nullable=False)
    refresh_token = Column(String, nullable=False)
