# ==========================================================
# OCR.PY
# AI Document Assistant
# Compatible with Python 3.13+
# ==========================================================

import easyocr
import numpy as np
from PIL import Image

# ==========================================================
# LOAD OCR MODEL
# ==========================================================

_reader = None


def get_reader():
    """
    Load EasyOCR model only once.
    """

    global _reader

    if _reader is None:

        _reader = easyocr.Reader(

            ['en'],

            gpu=False

        )

    return _reader


# ==========================================================
# OCR FROM IMAGE
# ==========================================================

def extract_text_from_image(image):

    """
    Extract text from a PIL Image.
    """

    reader = get_reader()

    image = np.array(image)

    results = reader.readtext(image)

    text = ""

    for result in results:

        text += result[1] + "\n"

    return text.strip()


# ==========================================================
# OCR FROM IMAGE FILE
# ==========================================================

def image_file_to_text(uploaded_file):

    """
    Read uploaded JPG/PNG image.
    """

    image = Image.open(uploaded_file)

    return extract_text_from_image(image)


# ==========================================================
# OCR FROM PDF IMAGES
# ==========================================================

def pdf_images_to_text(images):

    """
    OCR every image page of a scanned PDF.
    """

    final_text = ""

    for page in images:

        final_text += extract_text_from_image(page)

        final_text += "\n\n"

    return final_text.strip()


# ==========================================================
# DETECT IF OCR IS NEEDED
# ==========================================================

def needs_ocr(text):

    """
    Returns True if extracted PDF text is too small.
    """

    if text is None:

        return True

    if len(text.strip()) < 30:

        return True

    return False


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("EasyOCR Module Loaded Successfully")