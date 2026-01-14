from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud.user import get_user_by_id, signup_user
from app.schemas.chat import InvokeRequest
from app.utils.invoke import get_response, llm_invoke

from .database import get_db
from .crud import (
    get_users,
    create_user,
    create_chat,
    get_chats,
    get_chats_by_user_id,
)
from .schemas import UserCreate, UserResponse, ChatCreate, ChatResponse

# ------------------
# Users router
# ------------------
users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    return await signup_user(db, user)

@users_router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@users_router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)

@users_router.get("/{id}", response_model=list[UserResponse])
def get_user(db: Session = Depends(get_db), id: str = ""):
    return get_user_by_id(db, id)


# ------------------
# Chats router
# ------------------
chats_router = APIRouter(prefix="/chats", tags=["Chats"])

@chats_router.get("/", response_model=list[ChatResponse])
def list_chats(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_chats(db)

@chats_router.get("/user/{user_id}", response_model=list[ChatResponse])
def list_chats_by_user(user_id: str, db: Session = Depends(get_db)):
    return get_chats_by_user_id(db, user_id)

@chats_router.post("/invoke", response_model=str)
def invoke(invokerequest: InvokeRequest,db: Session = Depends(get_db)):
    response = llm_invoke(user_id=invokerequest.user_id, query=invokerequest.query, db=db)
    return response
    

# ------------------
# Ingestion router
# ------------------
from fastapi import UploadFile, File
import os
import shutil

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


ingestion_router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@ingestion_router.post("/")
async def ingest(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "File saved successfully"}