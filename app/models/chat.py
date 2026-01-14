from sqlalchemy import UUID, ForeignKey, String, TEXT
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from .user import User
from app.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(User.id), nullable=True)
    query: Mapped[str] = mapped_column(String, nullable=False)
    response: Mapped[str] = mapped_column(TEXT, nullable=False)
