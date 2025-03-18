# src/pdf_reader.py

import os
from typing import Optional
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

# Set the Tesseract OCR path if necessary (for Windows users)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Extracts text from a PDF file. Supports both normal text PDFs and scanned image-based PDFs using OCR.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF, or None if failed.
    """
    try:
        reader = PdfReader(pdf_path)
        extracted_text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"

        # If no text was extracted, attempt OCR (for scanned PDFs)
        if not extracted_text.strip():
            print(f"[Warning] No readable text found in {pdf_path}. Attempting OCR...")
            extracted_text = extract_text_with_ocr(pdf_path)

        if not extracted_text.strip():
            print(f"[Error] Unable to extract any text from {pdf_path}.")
            return None

        return extracted_text.strip()

    except Exception as e:
        print(f"[Error] PDF text extraction failed: {e}")
        return None

def extract_text_with_ocr(pdf_path: str) -> str:
    """
    Uses OCR (Tesseract) to extract text from scanned PDFs.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: Extracted text from the scanned PDF.
    """
    try:
        images = convert_from_path(pdf_path)
        ocr_text = ""

        for img in images:
            text = pytesseract.image_to_string(img)
            if text.strip():
                ocr_text += text + "\n"

        return ocr_text.strip()
    except Exception as e:
        print(f"[Error] OCR text extraction failed: {e}")
        return ""

if __name__ == "__main__":
    # Test code - Change the path to a real PDF
    test_pdf_path = "../data/NIPS-2017-attention-is-all-you-need-Paper.pdf"
    extracted_text = extract_text_from_pdf(test_pdf_path)

    if extracted_text:
        print("=== Extracted Text Preview ===")
        print(extracted_text[:1000])  # Show first 1000 characters
    else:
        print("❌ Failed to extract text.")
