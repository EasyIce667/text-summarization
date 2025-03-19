# src/ui.py
import gradio as gr
from pipeline import summarize_research_paper
import os
import shutil


def process_pdf(pdf_file, summary_length):
    """
    Process uploaded PDF and return summarized text based on user selection.

    Args:
        pdf_file: Uploaded PDF file object from Gradio.
        summary_length: Selected summary length option.

    Returns:
        str: Final summary
    """
    try:
        if pdf_file is None:
            return "❌ No file uploaded!"

        # Save uploaded file to temp directory
        temp_dir = "temp_upload"
        os.makedirs(temp_dir, exist_ok=True)
        temp_pdf_path = os.path.join(temp_dir, os.path.basename(pdf_file.name))

        shutil.copy(pdf_file.name, temp_pdf_path)

        # Adjust summarization parameters based on user choice
        length_options = {
            "Short": (80, 30),
            "Medium": (150, 50),
            "Long": (300, 100)
        }
        max_length, min_length = length_options.get(summary_length, (150, 50))

        # Run summarization pipeline
        summary = summarize_research_paper(
            temp_pdf_path,
            extractive_sentences=8,
            max_length=max_length,
            min_length=min_length
        )

        os.remove(temp_pdf_path)
        return summary if summary else "❌ Failed to generate summary. Please check the PDF content."

    except Exception as e:
        return f"❌ Error processing PDF: {e}"


# Gradio Interface
iface = gr.Interface(
    fn=process_pdf,
    inputs=[
        gr.File(label="Upload Research Paper (PDF)", file_types=[".pdf"]),
        gr.Radio(["Short", "Medium", "Long"], label="Summary Length", value="Medium")
    ],
    outputs="text",
    title="📄 Research Paper Summarizer (Extractive + Abstractive)",
    description="Upload a research paper PDF, choose summary length, and get a summarized version.",
    allow_flagging='never'
)

if __name__ == "__main__":
    iface.launch()
