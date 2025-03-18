# src/extractive.py

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from typing import Optional


def extractive_summary(text: str, sentences_count: int = 5) -> Optional[str]:
    """
    Performs extractive summarization on the input text using LexRank.

    Args:
        text (str): The full text to summarize.
        sentences_count (int): Number of sentences to include in the summary.

    Returns:
        str: Extracted key sentences as summary.
    """
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()

        summary = summarizer(parser.document, sentences_count)

        summarized_text = " ".join(str(sentence) for sentence in summary)

        if not summarized_text.strip():
            print("[Warning] Summary is empty, check input text length.")
            return None

        return summarized_text

    except Exception as e:
        print(f"[Error] Failed to generate extractive summary: {e}")
        return None


if __name__ == "__main__":
    # Test Example - you can replace this with real extracted text
    sample_text = """
    Natural Language Processing (NLP) is a subfield of artificial intelligence.
    It focuses on the interaction between computers and humans through language.
    NLP involves understanding, interpreting, and generating human languages.
    There are many applications like chatbots, translators, and summarizers.
    In this paper, we propose a novel approach to NLP-based summarization.
    """

    summary = extractive_summary(sample_text, sentences_count=3)
    if summary:
        print("=== Extractive Summary ===")
        print(summary)
    else:
        print("Failed to generate summary.")
