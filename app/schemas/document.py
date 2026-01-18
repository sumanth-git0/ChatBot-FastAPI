from typing import Any, Optional
from uuid import UUID
from pydantic import BaseModel

class DocumentCreate(BaseModel):
    user_id: UUID
    file_type: str
    file_name: str
    status: Optional[str] = 'Pending'

class DocumentUpdate(BaseModel):
    id: UUID
    status: Optional[str] = 'Success'

class DocumentResponse(DocumentCreate):
    id: UUID

    class Config:
        from_attributes = True

class DocumentRequest(BaseModel):
    user_id: UUID
    file: Any