# ==========================================================
# OCR.PY
# AI Document Assistant
# PyMuPDF + EasyOCR
# Compatible with Python 3.13+
# ==========================================================

import io

import fitz
import easyocr
import numpy as np

from PIL import Image

# ==========================================================
# LOAD OCR MODEL
# ==========================================================

_reader = None


def get_reader():

    global _reader

    if _reader is None:

        _reader = easyocr.Reader(

            ["en"],

            gpu=False

        )

    return _reader


# ==========================================================
# OCR FROM PIL IMAGE
# ==========================================================

def extract_text_from_image(image):

    reader = get_reader()

    image = np.array(image)

    results = reader.readtext(image)

    text = ""

    for result in results:

        text += result[1]

        text += "\n"

    return text.strip()


# ==========================================================
# OCR FROM IMAGE FILE
# ==========================================================

def image_file_to_text(uploaded_file):

    image = Image.open(uploaded_file)

    return extract_text_from_image(image)


# ==========================================================
# OCR FROM SCANNED PDF
# ==========================================================

def extract_text_from_scanned_pdf(uploaded_file):

    try:

        uploaded_file.seek(0)

        pdf_bytes = uploaded_file.read()

        document = fitz.open(

            stream=pdf_bytes,

            filetype="pdf"

        )

        final_text = ""

        for page in document:

            pix = page.get_pixmap(

                dpi=300

            )

            image_bytes = pix.tobytes(

                "png"

            )

            image = Image.open(

                io.BytesIO(

                    image_bytes

                )

            )

            page_text = extract_text_from_image(

                image

            )

            final_text += page_text

            final_text += "\n\n"

        document.close()

        return final_text.strip()

    except Exception as e:

        raise Exception(

            f"OCR Error:\n{e}"

        )


# ==========================================================
# OCR FROM PAGE IMAGES
# ==========================================================

def pdf_images_to_text(images):

    text = ""

    for image in images:

        text += extract_text_from_image(

            image

        )

        text += "\n\n"

    return text.strip()


# ==========================================================
# DETECT SCANNED PDF
# ==========================================================

def needs_ocr(text):

    if text is None:

        return True

    if len(text.strip()) < 30:

        return True

    return False


# ==========================================================
# OCR INFORMATION
# ==========================================================

def ocr_info():

    return {

        "engine": "EasyOCR",

        "pdf_engine": "PyMuPDF",

        "gpu": False

    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print(

        "OCR Module Loaded Successfully"

    )

    print(

        ocr_info()

    )
