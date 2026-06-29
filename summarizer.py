# ==========================================================
# AI SUMMARIZER
# Compatible with Python 3.13+
# ==========================================================

import torch
from transformers import pipeline


class AISummarizer:

    def __init__(self):

        self.device = 0 if torch.cuda.is_available() else -1

        self.model = pipeline(
            task="summarization",
            model="facebook/bart-large-cnn",
            device=self.device
        )

    # ======================================================
    # Split Large Documents
    # ======================================================

    def split_text(self, text, max_words=800):

        words = text.split()

        chunks = []

        for i in range(0, len(words), max_words):

            chunk = " ".join(words[i:i + max_words])

            chunks.append(chunk)

        return chunks

    # ======================================================
    # Generate Summary
    # ======================================================

    def summarize(self, text, summary_type="Medium"):

        if not text.strip():

            return ""

        summary_type = summary_type.lower()

        if summary_type == "short":

            max_length = 60
            min_length = 20

        elif summary_type == "long":

            max_length = 220
            min_length = 80

        else:

            max_length = 120
            min_length = 40

        chunks = self.split_text(text)

        summaries = []

        try:

            for chunk in chunks:

                result = self.model(

                    chunk,

                    max_length=max_length,

                    min_length=min_length,

                    do_sample=False,

                    truncation=True

                )

                summaries.append(result[0]["summary_text"])

            final_summary = " ".join(summaries)

            return final_summary

        except Exception as e:

            return f"Summary Error: {e}"


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    ai = AISummarizer()

    sample = """
    Artificial Intelligence is transforming the world.
    It enables computers to perform tasks that usually
    require human intelligence.
    AI is widely used in healthcare, finance,
    agriculture, education, transportation,
    robotics and cybersecurity.
    """

    print(ai.summarize(sample, "Medium"))