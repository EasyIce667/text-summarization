# src/abstractive.py


import time
start_time = time.time()

from transformers import pipeline
from typing import Optional

# facebook/bart-large-cnn
# t5-small
# google/pegasus-xsum

# Load model globally to avoid reloading for each call (slow otherwise)
summarizer_pipeline = pipeline("summarization", model="google/pegasus-xsum")


def abstractive_summary(text: str, max_length: int = 150, min_length: int = 40) -> Optional[str]:
    """
    Generates an abstractive summary of the input text using BART.

    Args:
        text (str): Full text to summarize.
        max_length (int): Maximum length of the summary.
        min_length (int): Minimum length of the summary.

    Returns:
        str: The abstractive summary.
    """
    try:
        if not text.strip():
            print("[Warning] Input text is empty.")
            return None

        # Summarize using pipeline
        summary_list = summarizer_pipeline(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )

        return summary_list[0]['summary_text'].strip()

    except Exception as e:
        print(f"[Error] Failed to generate abstractive summary: {e}")
        return None


if __name__ == "__main__":
    # Test Example - You can replace this with real extracted text
    sample_text = """
    Natural Language Processing (NLP) is a subfield of artificial intelligence.
    It focuses on the interaction between computers and humans through language.
    NLP involves understanding, interpreting, and generating human languages.
    There are many applications like chatbots, translators, and summarizers.
    In this paper, we propose a novel approach to NLP-based summarization that improves upon previous methods.
    """

    summary = abstractive_summary(sample_text, max_length=100, min_length=30)
    if summary:
        print("=== Abstractive Summary ===")
        print(summary)
    else:
        print("Failed to generate summary.")


end_time = time.time()
print(f"Execution Time: {end_time - start_time:.4f} seconds")