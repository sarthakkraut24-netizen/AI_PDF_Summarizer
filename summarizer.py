# ==========================================================
# SUMMARIZER.PY
# AI Document Assistant
# Gemini AI Summarizer
# Compatible with Python 3.13+
# ==========================================================

import os

import google.generativeai as genai

from dotenv import load_dotenv

from utils import split_text


# ==========================================================
# LOAD API KEY
# ==========================================================

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env file."
    )

genai.configure(api_key=API_KEY)


# ==========================================================
# AI SUMMARIZER
# ==========================================================

class AISummarizer:

    def __init__(self):

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    # ======================================================
    # GENERATE SUMMARY
    # ======================================================

    def summarize(
        self,
        text,
        summary_type="Medium"
    ):

        if not text.strip():

            return "No text found."

        summary_type = summary_type.lower()

        if summary_type == "short":

            instruction = """
            Summarize in 5-6 bullet points.
            Keep it concise.
            """

        elif summary_type == "long":

            instruction = """
            Generate a detailed summary.
            Include every important point.
            """

        else:

            instruction = """
            Generate a medium-length summary.
            Cover all important information.
            """

        chunks = split_text(
            text,
            chunk_size=1800
        )

        summaries = []

        try:

            for chunk in chunks:

                prompt = f"""
                {instruction}

                Document:

                {chunk}
                """

                response = self.model.generate_content(
                    prompt
                )

                summaries.append(
                    response.text.strip()
                )

            if len(summaries) == 1:

                return summaries[0]

            final_prompt = f"""
            Combine these summaries into one
            well-structured summary.

            {' '.join(summaries)}
            """

            final_summary = self.model.generate_content(
                final_prompt
            )

            return final_summary.text.strip()

        except Exception as e:

            return f"Summary Error: {e}"


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    ai = AISummarizer()

    sample = """
    Artificial Intelligence is transforming
    healthcare, education, finance and
    transportation by automating tasks,
    improving decision making and increasing
    productivity.
    """

    print(

        ai.summarize(

            sample,

            "Medium"

        )

    )