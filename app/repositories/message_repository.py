from typing import Optional
from sqlalchemy import func
from sqlmodel import Session, select
from app.models.orm import Message

class MessageRepository:
    """Repository for managing Message entities in the database."""
    def __init__(self, session: Session):
        self.session = session

    def create(self, message: Message) -> Message:
        """Create and store a new message in the database.
        Args:
            message (Message)

        Returns:
            Message
        """
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_by_session(
        self, session_id: str,
        limit: int = 50,
        offset: int = 0,
        sender: Optional[str] = None
    ) -> tuple[int, list[Message]]:
        """Get messages by session ID with pagination and optional sender filtering.

        Args:
            session_id (str): session
            limit (int, optional): limit. Defaults to 50.
            offset (int, optional): limit. Defaults to 0.
            sender (Optional[str], optional): sender. Defaults to None.

        Returns:
            tuple[int, list[Message]]: result
        """
        if limit < 0 or offset < 0:
            raise ValueError("Limit and offset must be non-negative")

        base_query = select(Message).where(Message.session_id == session_id)
        if sender:
            base_query = base_query.where(Message.sender == sender)

        total_query = select(func.count(Message.id)).where(Message.session_id == session_id)
        if sender:
            total_query = total_query.where(Message.sender == sender)

        total = self.session.exec(total_query).one_or_none() or 0
        messages = self.session.exec(base_query.offset(offset).limit(limit)).all()

        return total, messages
