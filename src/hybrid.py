# src/hybrid.py
import time
start_time = time.time()

from extractive import extractive_summary
from abstractive import abstractive_summary
from typing import Optional


def hybrid_summary(text: str, extractive_sentences: int = 10,
                   max_length: int = 150, min_length: int = 40) -> Optional[str]:
    """
    Combines extractive and abstractive summarization for better results.

    Args:
        text (str): Full input text to summarize.
        extractive_sentences (int): Number of sentences for extractive summarization.
        max_length (int): Max length of final abstractive summary.
        min_length (int): Min length of final abstractive summary.

    Returns:
        str: Final combined summary or None if failed
    """
    try:
        print("\n[Step 1] Running Extractive Summarization...")
        extracted_text = extractive_summary(text, sentences_count=extractive_sentences)
        if not extracted_text:
            print("[Error] Extractive summary failed.")
            return None

        print("\n[Step 2] Running Abstractive Summarization on Extracted Text...")
        final_summary = abstractive_summary(extracted_text, max_length=max_length, min_length=min_length)
        if not final_summary:
            print("[Error] Abstractive summary failed.")
            return None

        return final_summary

    except Exception as e:
        print(f"[Error] Hybrid summarization failed: {e}")
        return None


if __name__ == "__main__":
    # Test Example - You can replace this with real extracted text
    sample_text = """
    Natural Language Processing (NLP) is a subfield of artificial intelligence that focuses on the interaction between computers and humans using natural language.
    The ultimate goal of NLP is to read, decipher, understand, and make sense of human language in a manner that is valuable.
    Techniques such as sentiment analysis, machine translation, and summarization have made significant progress in recent years.
    We present a hybrid approach to text summarization that first extracts key sentences and then rewrites them into a fluent paragraph.
    """

    summary = hybrid_summary(sample_text, extractive_sentences=3, max_length=100, min_length=30)
    if summary:
        print("\n=== Hybrid Summary ===")
        print(summary)
    else:
        print("Failed to generate hybrid summary.")

end_time = time.time()
print(f"Execution Time: {end_time - start_time:.4f} seconds")