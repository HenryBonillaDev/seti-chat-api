from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlmodel import Session
from app.api.v1.schemas import CreateMessage, MessageSuccessResponse, PaginatedMessageSuccessResponse, PaginatedMessages
from app.core.exceptions import InternalServerError, InvalidFormatException
from app.services.message_service import MessageService
from app.core.db import get_session

router = APIRouter()

@router.post("/messages", response_model=MessageSuccessResponse, status_code=status.HTTP_201_CREATED)
def create_message(payload: CreateMessage, session: Session = Depends(get_session)):
    if payload.sender not in ["user", "system"]:
        raise InvalidFormatException(details="El campo 'sender' debe ser 'user' o 'system'")
    try:
        service = MessageService(session)
        resData = service.process_and_store(payload)
        return MessageSuccessResponse(data=resData)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="El mensaje ya existe.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/messages/{session_id}", response_model=PaginatedMessageSuccessResponse)
def get_messages(
    session_id: str,
    limit: int = Query(50, gt=0, le=200),
    offset: int = Query(0, ge=0),
    sender: str | None = None,
    session: Session = Depends(get_session)
):
    try:
        service = MessageService(session)
        paginated_messages = service.get_messages(session_id, limit, offset, sender)
        return PaginatedMessageSuccessResponse(data=paginated_messages)
    except ValueError as e:
        raise InvalidFormatException("Argumento invalido")
    except Exception as e:
        raise InternalServerError("Ocurrió un error inesperado. Por favor, intenta de nuevo más tarde.")

