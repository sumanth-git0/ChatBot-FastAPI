import os

from app.ingestion.document import extract_text_from_docx
from app.ingestion.pdf_page_as_image import extract_text_from_scanned_pdf
from app.ingestion.pdf_text_only import extract_text_from_pdf

async def extract_text(file_path):
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

