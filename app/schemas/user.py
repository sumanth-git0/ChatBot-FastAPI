from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: Optional[str] = ""

class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True
