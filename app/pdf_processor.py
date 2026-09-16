from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extract text from every page of a PDF.

    Returns:
        A list containing the page number and extracted text.
    """

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append({
                "page": page_number,
                "text": text.strip()
            })

    return pages