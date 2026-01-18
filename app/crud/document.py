from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate


def create_document(db: Session, document: DocumentCreate):
    db_document = Document(user_id=document.user_id, file_name=document.file_name, file_type=document.file_type, status=document.status)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def update_document(db: Session, document_update: DocumentUpdate):
    db_document = db.query(Document).filter(Document.id == document_update.id).first()

    if not db_document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document_update.status is not None:
        db_document.status = document_update.status

    db.commit()
    db.refresh(db_document)
    return db_document
    

def get_documents(db: Session):
    return db.query(Document).all()

def get_documents_by_user_id(db: Session, user_id: str):
    return db.query(Document).filter(Document.user_id == user_id).all()
