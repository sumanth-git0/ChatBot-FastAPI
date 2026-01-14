import pytesseract
from pdf2image import convert_from_path

def extract_text_from_scanned_pdf(path):
    pages = convert_from_path(path)
    text = ""
    for img in pages:
        text += pytesseract.image_to_string(img)
    return text.strip()
