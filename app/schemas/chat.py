from pydantic import BaseModel

class ChatCreate(BaseModel):
    user_id: int
    query: str
    response: str

class ChatResponse(ChatCreate):
    id: int

    class Config:
        from_attributes = True


class InvokeRequest(BaseModel):
    user_id: int
    query: str