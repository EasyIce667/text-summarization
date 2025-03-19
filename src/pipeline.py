# src/pipeline.py

from pdf_reader import extract_text_from_pdf
from hybrid import hybrid_summary
from typing import Optional
from pdf2image import convert_from_path
import pytesseract


def ocr_extract_text(pdf_path: str) -> str:
    """
    Extract text from an image-based PDF using OCR.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from images.
    """
    images = convert_from_path(pdf_path)
    extracted_text = ""

    for img in images:
        extracted_text += pytesseract.image_to_string(img)

    return extracted_text.strip()


def summarize_research_paper(pdf_path: str, extractive_sentences: int = 10,
                             max_length: int = 150, min_length: int = 40) -> Optional[str]:
    """
    Full pipeline: PDF file -> Text extraction -> Hybrid summarization -> Final summary.

    Args:
        pdf_path (str): Path to the PDF file.
        extractive_sentences (int): Number of extractive sentences.
        max_length (int): Max length of final summary.
        min_length (int): Min length of final summary.

    Returns:
        str: Final summarized text or None if failed.
    """
    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        text = ocr_extract_text(pdf_path)

    if not text:
        return "❌ No readable text found in PDF."

    return hybrid_summary(text, extractive_sentences=extractive_sentences, max_length=max_length, min_length=min_length)


if __name__ == "__main__":
    test_pdf_path = "../data/NIPS-2017-attention-is-all-you-need-Paper.pdf"  # Replace with real file path
    final_summary = summarize_research_paper(
        test_pdf_path,
        extractive_sentences=50,
        max_length=1000,
        min_length=100
    )

    if final_summary:
        print("\n=== Final Research Paper Summary ===")
        print(final_summary)
    else:
        print("Failed to generate final summary.")
