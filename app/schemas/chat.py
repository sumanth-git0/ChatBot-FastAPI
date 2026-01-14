from uuid import UUID
from pydantic import BaseModel

class ChatCreate(BaseModel):
    user_id: UUID
    query: str
    response: str

class ChatResponse(ChatCreate):
    id: UUID

    class Config:
        from_attributes = True


class InvokeRequest(BaseModel):
    user_id: UUID
    query: str