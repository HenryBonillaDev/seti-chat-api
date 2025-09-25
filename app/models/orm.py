from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True)
    message_id: str = Field(index=True, nullable=False)
    session_id: str = Field(index=True, nullable=False)
    content: str = Field(nullable=False)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sender: str = Field(nullable=False)
    length: int = Field(nullable=True)
    word_count: int = Field(nullable=True)

    __table_args__ = (
        UniqueConstraint('session_id', 'message_id', name='uix_message_session'),
    )
