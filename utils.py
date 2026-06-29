# ==========================================================
# UTILITY FUNCTIONS
# Compatible with Python 3.13+
# ==========================================================

import os
import re
from datetime import datetime

# ==========================================================
# PROJECT FOLDERS
# ==========================================================

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
HISTORY_FOLDER = "history"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(HISTORY_FOLDER, exist_ok=True)

HISTORY_FILE = os.path.join(HISTORY_FOLDER, "history.txt")

# ==========================================================
# WORD COUNT
# ==========================================================

def word_count(text):

    if not text:
        return 0

    return len(text.split())


# ==========================================================
# CHARACTER COUNT
# ==========================================================

def character_count(text):

    if not text:
        return 0

    return len(text)


# ==========================================================
# SENTENCE COUNT
# ==========================================================

def sentence_count(text):

    if not text:
        return 0

    sentences = re.split(r"[.!?]+", text)

    return len([s for s in sentences if s.strip()])


# ==========================================================
# PARAGRAPH COUNT
# ==========================================================

def paragraph_count(text):

    if not text:
        return 0

    paragraphs = text.split("\n\n")

    return len([p for p in paragraphs if p.strip()])


# ==========================================================
# READING TIME
# ==========================================================

def reading_time(text):

    words = word_count(text)

    return max(1, round(words / 200))


# ==========================================================
# COMPRESSION PERCENTAGE
# ==========================================================

def compression_percentage(original, summary):

    original_words = word_count(original)
    summary_words = word_count(summary)

    if original_words == 0:

        return 0

    percentage = (
        (original_words - summary_words)
        / original_words
    ) * 100

    return round(percentage, 2)


# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text):

    if not text:

        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================================
# SAVE SUMMARY
# ==========================================================

def save_summary(summary):

    if not summary:

        return None

    filename = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    filepath = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(summary)

    return filepath


# ==========================================================
# SAVE HISTORY
# ==========================================================

def save_history(original_text, summary):

    with open(
        HISTORY_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write("=" * 80 + "\n")
        file.write(f"Date : {datetime.now()}\n\n")

        file.write("ORIGINAL TEXT\n")
        file.write(original_text)

        file.write("\n\nSUMMARY\n")
        file.write(summary)

        file.write("\n\n")


# ==========================================================
# LOAD HISTORY
# ==========================================================

def load_history():

    if not os.path.exists(HISTORY_FILE):

        return "No history available."

    with open(
        HISTORY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ==========================================================
# CLEAR HISTORY
# ==========================================================

def clear_history():

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("")


# ==========================================================
# FILE SIZE
# ==========================================================

def file_size(file):

    if file is None:

        return 0

    return round(file.size / 1024, 2)


# ==========================================================
# FILE EXTENSION
# ==========================================================

def file_extension(file):

    if file is None:

        return ""

    return os.path.splitext(file.name)[1].lower()


# ==========================================================
# PROJECT INFORMATION
# ==========================================================

def project_info():

    return {

        "Project": "AI Document Assistant",

        "Version": "3.0",

        "Developer": "Sarthak Raut",

        "Framework": "Streamlit",

        "Language": "Python 3.13",

        "Database": "SQLite",

        "AI Model": "facebook/bart-large-cnn",

        "Chat Model": "Gemini 2.5 Flash"

    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    sample = """
    Artificial Intelligence is transforming the world.
    It enables machines to perform intelligent tasks.
    """

    print("Words :", word_count(sample))
    print("Characters :", character_count(sample))
    print("Sentences :", sentence_count(sample))
    print("Paragraphs :", paragraph_count(sample))
    print("Reading Time :", reading_time(sample), "minute(s)")
    print("Project Info :", project_info())