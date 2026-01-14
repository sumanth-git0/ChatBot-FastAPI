import os

from app.ingestion.document import extract_text_from_docx
from app.ingestion.pdf_page_as_image import extract_text_from_scanned_pdf
from app.ingestion.pdf_text_only import extract_text_from_pdf

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
        if len(text) < 100:
            text = extract_text_from_scanned_pdf(file_path)
        return text

    elif ext == ".docx":
        return extract_text_from_docx(file_path)

    else:
        raise ValueError("Unsupported file type")


# def ingest_document(file_path):
#     text = extract_text(file_path)
#     chunks = chunk_text(text)
#     vector_store.add_texts(chunks)


# def retrieve_context(question, k=5):
#     docs = vector_store.similarity_search(question, k=k)
#     return "\n\n".join(d.page_content for d in docs)
