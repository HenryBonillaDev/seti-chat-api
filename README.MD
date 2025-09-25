### Objetivo del proyecto
Desarrollar una API de un chat

- Requisitos (Python, pip)

## Docker
- docker build .
- docker compose up -d
- **Swagger:** `http://localhost:8000/docs` - En swagger se pueden  probar los endpoint
- **Ejecutar Pruebas:** `docker compose exec -it web pytest --cov=app --cov-report=term-missing`

## Cómo correr local:

- python -m venv .venv && source .venv/bin/activate

- pip install -r requirements.txt

- uvicorn app.main:app --reload

- link a Swagger: http://localhost:8000/docs

## Endpoints y ejemplo de payload

### **1\. Crear un mensaje**

Crea y almacena un mensaje dentro de una sesión.

-   **URL:** `POST /api/messages`
-   **Request Body (`application/json`):**


```
{
  "message_id": "msg_12345",
  "session_id": "sess_67890",
  "content": "Hola, este es un mensaje de prueba",
  "timestamp": "2025-09-24T22:00:00Z",
  "sender": "user"
}
```

-   **Response `201 CREATED`:**
```
{
  "status": "success",
  "data": {
    "message_id": "msg_12345",
    "session_id": "sess_67890",
    "content": "Hola, este es un mensaje de prueba",
    "timestamp": "2025-09-24T22:00:00Z",
    "sender": "user",
    "metadata": {
      "word_count": 7,
      "character_count": 41,
      "processed_at": "2025-09-24T22:01:00Z"
    }
  }
}
```

### **2\. Listar mensajes de una sesión**

Obtiene una lista paginada de mensajes para una sesión específica.

-   **URL:**  `GET /api/messages/{session_id}`

-  **Response** `200 OK`:
```
{
  "status": "success",
  "data": {
    "total": 2,
    "limit": 50,
    "offset": 0,
    "items": [
      {
        "message_id": "msg_12345",
        "session_id": "sess_67890",
        "content": "Hola, este es un mensaje de prueba",
        "timestamp": "2025-09-24T22:00:00Z",
        "sender": "user",
        "metadata": {
          "word_count": 7,
          "character_count": 41,
          "processed_at": "2025-09-24T22:01:00Z"
        }
      },
      {
        "message_id": "msg_12346",
        "session_id": "sess_67890",
        "content": "Respuesta automática",
        "timestamp": "2025-09-24T22:02:00Z",
        "sender": "system",
        "metadata": {
          "word_count": 2,
          "character_count": 21,
          "processed_at": "2025-09-24T22:03:00Z"
        }
      }
    ]
  }
}

```

## Cómo ejecutar tests:

- pytest --cov=app --cov-report=term-missing
