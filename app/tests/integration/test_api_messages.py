from datetime import datetime, timezone

from app.api.v1.schemas import MessageSuccessResponse

def test_create_and_get_messages(client):
    payload = {
        "session_id": "session123",
        "message_id": "msg-1",
        "sender": "user",
        "content": "Hola desde integración",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    response = client.post("/api/messages", json=payload)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["session_id"] == "session123"

    response = client.get("/api/messages/session123")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["content"] == "Hola desde integración"


def test_create_duplicate_message(client):
    payload = {
        "session_id": "session123",
        "message_id": "msg-dup",
        "sender": "user",
        "content": "Mensaje original",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    response = client.post("/api/messages", json=payload)
    assert response.status_code == 201
    response = client.post("/api/messages", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "El mensaje ya existe."

def test_create_message_missing_fields(client):
    payload = {
        "session_id": "session123",
        "message_id": "msg-missing",
        "content": "Falta el remitente",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    response = client.post("/api/messages", json=payload)
    assert response.status_code == 422 

def test_create_message_invalid_field(client):
    payload = {
        "session_id": "session123",
        "message_id": "msg-invalid-ts",
        "sender": "user",
        "content": "Timestamp inválido",
        "timestamp": "invalid-timestamp"
    }
    response = client.post("/api/messages", json=payload)
    assert response.status_code == 422