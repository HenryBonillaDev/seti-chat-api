from sqlalchemy import select
from datetime import datetime, timezone
from app.api.v1.schemas import CreateMessage
from app.services.message_service import MessageService
from app.models.orm import Message

def test_process_and_store_creates_message(db_session):
    service = MessageService(db_session)

    payload = CreateMessage(
        session_id="test-process-store",
        message_id="1",
        sender="user",
        content="Hola mundo",
        timestamp=datetime(2024, 10, 1, 12, 0, 0, tzinfo=timezone.utc)
    )

    result = service.process_and_store(payload)

    assert result.session_id == payload.session_id
    assert result.message_id == payload.message_id

    stmt = select(Message).where(
    Message.session_id == payload.session_id,
    Message.message_id == payload.message_id
    )

    db_item = db_session.execute(stmt).scalars().first()

    assert db_item is not None
    assert db_item.content == "Hola mundo"
