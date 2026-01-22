from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from app.models.chunks import Chunk
from app.utils.file_ingestion import extract_text

async def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_text(text)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



async def ingest_document(file_path, document_id: str, user_id: str, db):
    text = await extract_text(file_path)
    chunked_text = await chunk_text(text)

    for i, chunk in enumerate(chunked_text):
        embedding = embeddings.embed_documents([chunk])[0]

        db_chunk = Chunk(
            document_id=document_id,
            user_id=user_id,
            source_id=file_path,
            chunk_index=i,
            content=chunk,
            embedding=embedding,
        )
        db.add(db_chunk)
    db.commit()