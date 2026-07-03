# ==========================================================
# UTILS.PY
# AI Document Assistant
# Compatible with Python 3.13+
# ==========================================================

import re
import os
import string
from datetime import datetime


# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text: str) -> str:
    """
    Cleans extracted document text.
    """

    if not text:
        return ""

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


# ==========================================================
# REMOVE SPECIAL CHARACTERS
# ==========================================================

def remove_special_characters(text: str) -> str:
    """
    Removes unnecessary special characters.
    """

    allowed = string.ascii_letters + string.digits + " .,!?():;%$@#/-\n"

    cleaned = "".join(ch for ch in text if ch in allowed)

    return cleaned


# ==========================================================
# WORD COUNT
# ==========================================================

def word_count(text: str) -> int:

    if not text:
        return 0

    return len(text.split())


# ==========================================================
# CHARACTER COUNT
# ==========================================================

def character_count(text: str) -> int:

    if not text:
        return 0

    return len(text)


# ==========================================================
# ESTIMATED READING TIME
# ==========================================================

def reading_time(text: str) -> int:
    """
    Average reading speed = 200 words/minute
    """

    words = word_count(text)

    minutes = max(1, round(words / 200))

    return minutes


# ==========================================================
# CURRENT DATE & TIME
# ==========================================================

def current_datetime():

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ==========================================================
# FILE SIZE
# ==========================================================

def file_size(file) -> float:
    """
    Returns uploaded file size in KB.
    """

    if file is None:
        return 0

    return round(file.size / 1024, 2)


# ==========================================================
# FILE EXTENSION
# ==========================================================

def file_extension(filename: str) -> str:

    return os.path.splitext(filename)[1].lower()


# ==========================================================
# VALIDATE FILE
# ==========================================================

SUPPORTED_FILES = [
    ".pdf",
    ".docx",
    ".txt",
    ".pptx",
    ".xlsx",
    ".png",
    ".jpg",
    ".jpeg"
]


def is_supported(filename: str) -> bool:

    return file_extension(filename) in SUPPORTED_FILES


# ==========================================================
# SPLIT LARGE TEXT
# ==========================================================

def split_text(text: str, chunk_size: int = 800):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunks.append(" ".join(words[i:i + chunk_size]))

    return chunks


# ==========================================================
# SUCCESS MESSAGE
# ==========================================================

def success(message):

    return f"✅ {message}"


# ==========================================================
# ERROR MESSAGE
# ==========================================================

def error(message):

    return f"❌ {message}"


# ==========================================================
# INFO MESSAGE
# ==========================================================

def info(message):

    return f"ℹ️ {message}"


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    sample = """
    Artificial Intelligence is transforming industries.
    AI improves automation, decision making and productivity.
    """

    print("Clean Text:")
    print(clean_text(sample))

    print("\nWord Count:", word_count(sample))
    print("Character Count:", character_count(sample))
    print("Reading Time:", reading_time(sample), "minute(s)")
    print("Current Date:", current_datetime())