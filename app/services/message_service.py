from sqlmodel import Session
from app.api.v1.schemas import CreateMessage, MessageData, MessageMetadata, PaginatedMessages
from app.core.exceptions import InvalidFormatException
from app.models.orm import Message
from app.repositories.message_repository import MessageRepository
from app.utils.filter import is_inappropriate_content
from datetime import datetime, timezone

class MessageService:
    def __init__(self, session: Session):
        self.repo = MessageRepository(session)

    def process_and_store(self, payload:CreateMessage) -> MessageData:
        """
        Process and store
        """
        if is_inappropriate_content(payload.content):
            raise InvalidFormatException("El mensaje contiene contenido inapropiado")

        metadata = MessageMetadata(
            word_count=len(payload.content.split()),
            character_count=len(payload.content),
            processed_at=datetime.now(timezone.utc)
        )

        message = Message(
            message_id=payload.message_id,
            session_id=payload.session_id,
            content=payload.content,
            timestamp=payload.timestamp,
            sender=payload.sender,
            length=metadata.character_count,
            word_count=metadata.word_count
        )

        self.repo.create(message)

        return MessageData(
            message_id=message.message_id,
            session_id=message.session_id,
            content=message.content,
            timestamp=message.timestamp,
            sender=message.sender,
            metadata=metadata
        )
    
    def get_messages(
        self,
        session_id: str,
        limit: int,
        offset: int,
        sender: str | None
    ) -> PaginatedMessages:
        """
        Obtiene los mensajes paginados filtrados por sesión y, opcionalmente, por sender.
        """
        total, messages = self.repo.get_by_session(session_id, limit, offset, sender)

        items = [
            MessageData(
                message_id=msg.message_id,
                session_id=msg.session_id,
                content=msg.content,
                timestamp=msg.timestamp,
                sender=msg.sender,
                metadata=MessageMetadata(
                    word_count=msg.word_count,
                    character_count=msg.length,
                    processed_at=datetime.now(timezone.utc)
                )
            )
            for msg in messages
        ]

        return PaginatedMessages(
            total=total,
            limit=limit,
            offset=offset,
            items=items
        )

