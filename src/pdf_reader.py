# src/pdf_reader.py

from PyPDF2 import PdfReader
from typing import Optional


def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF, or None if failed.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        if not text.strip():
            print(f"[Warning] No text extracted from {pdf_path}")
            return None

        return text

    except Exception as e:
        print(f"[Error] Failed to extract text from PDF: {e}")
        return None


if __name__ == "__main__":
    # Test code - you can remove this part in production
    test_pdf_path = '/Users/hardik/Desktop/Text Summarization /data/2306.07303v1.pdf'  # Replace with your real file path
    extracted_text = extract_text_from_pdf(test_pdf_path)

    if extracted_text:
        print("=== Extracted Text Preview ===")
        print(extracted_text[:1000])  # Print first 1000 characters to check
    else:
        print("Failed to extract text.")
