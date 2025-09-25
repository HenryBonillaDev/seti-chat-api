from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class CreateMessage(BaseModel):
    message_id: str = Field(..., description="ID único del mensaje")
    session_id: str = Field(..., description="ID único de la sesión")
    content: str = Field(..., description="Contenido del mensaje")
    timestamp: datetime = Field(..., description="Fecha y hora del mensaje")
    sender: Literal["user", "system"] = Field(..., description="Remitente ('user' o 'system')")

class MessageMetadata(BaseModel):
    word_count: int
    character_count: int
    processed_at: datetime

class MessageData(BaseModel):
    message_id: str = Field(..., description="ID único del mensaje")
    session_id: str = Field(..., description="ID único de la sesión")
    content: str = Field(..., description="Contenido del mensaje")
    timestamp: datetime = Field(..., description="Fecha y hora del mensaje")
    sender: Literal["user", "system"] = Field(..., description="Remitente ('user' o 'system')")
    metadata: MessageMetadata

class MessageSuccessResponse(BaseModel):
    status: Literal["success"] = "success"
    data: MessageData


class PaginatedMessages(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[MessageData]

class PaginatedMessageSuccessResponse(BaseModel):
    status: Literal["success"] = "success"
    data: PaginatedMessages