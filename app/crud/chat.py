from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.schemas.chat import ChatCreate


def create_chat(db: Session, chat: ChatCreate):
    db_user = Chat(user_id=chat.user_id, query=chat.query, response=chat.response)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_chats(db: Session):
    return db.query(Chat).all()

def get_chats_by_user_id(db: Session, user_id: str):
    return db.query(Chat).filter(Chat.user_id == user_id).all()
