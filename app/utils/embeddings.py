from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from app.utils.file_ingestion import extract_text

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_text(text)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def getvector_store(vector_store):
    if vector_store is None:
        vector_store = FAISS.from_texts([], embeddings)
    return vector_store

def ingest_document(file_path, vector_store=None):
    text = extract_text(file_path)
    chunks = chunk_text(text)

    if vector_store is None:
        vector_store = FAISS.from_texts(chunks, embeddings)
    else:
        vector_store.add_texts(chunks)

    return vector_store



def retrieve_context(question, vector_store, k=5):
    docs = vector_store.similarity_search(question, k=k)
    return "\n\n".join(d.page_content for d in docs)