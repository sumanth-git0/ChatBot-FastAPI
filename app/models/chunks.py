from app.models.user import User
from .document import Document
from sqlalchemy import UUID, ForeignKey, Integer, String, TEXT
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base
from pgvector.sqlalchemy import Vector


class Chunk(Base):
    __tablename__ = 'chunks'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(User.id),
        nullable=False,
        index=True
    )
    source_id: Mapped[str] = mapped_column(String, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(TEXT, nullable=False)
    meta_data: Mapped[dict] = mapped_column(JSONB, nullable=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(384))