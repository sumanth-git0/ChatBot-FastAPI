from .document import Document
from sqlalchemy import UUID, ForeignKey, Integer, String, TEXT
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class Chunk(Base):
    __tablename__ = 'chunks'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Document.id), nullable=True)
    source_id: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(TEXT, nullable=True)
    meta_data: Mapped[dict] = mapped_column(JSONB, nullable=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=True)