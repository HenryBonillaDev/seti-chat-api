import pytest
from app.repositories.message_repository import MessageRepository
from app.models.orm import Message

def test_get_by_session_returns_messages(db_session):
    repo = MessageRepository(db_session)

    msg1 = Message(session_id="abc123", message_id=1, sender="user", content="Hola")
    msg2 = Message(session_id="abc123", message_id=2, sender="system", content="Respuesta")
    db_session.add_all([msg1, msg2])
    db_session.commit()

    total, items = repo.get_by_session("abc123", limit=10, offset=0, sender=None)
    assert total == 2
    assert len(items) == 2
    assert items[0].content == "Hola"

def test_get_by_session_negative_limit_and_offset(db_session):
    repo = MessageRepository(db_session)

    msg = Message(session_id="Negative", message_id=3, sender="user", content="Hola")
    db_session.add(msg)
    db_session.commit()

    with pytest.raises(ValueError, match="Limit and offset must be non-negative"):
        repo.get_by_session(msg.session_id, -10, 10)

def test_get_by_session_with_sender(db_session):
    repo = MessageRepository(db_session)

    msg1 = Message(session_id="TestSession", message_id=1, sender="user1", content="Hola de user1")
    msg2 = Message(session_id="TestSession", message_id=2, sender="user2", content="Hola de user2")
    msg3 = Message(session_id="TestSession", message_id=3, sender="user1", content="Otro mensaje de user1")
    db_session.add_all([msg1, msg2, msg3])
    db_session.commit()

    total, messages = repo.get_by_session(session_id="TestSession", limit=10, offset=0, sender="user1")

    assert total == 2
    assert len(messages) == 2
    assert all(msg.sender == "user1" for msg in messages)
    assert {msg.message_id for msg in messages} == {"1", "3"}