# ==========================================================
# FILE READER
# Compatible with Python 3.13+
# ==========================================================

import os
from pypdf import PdfReader
from docx import Document


# ==========================================================
# READ PDF
# ==========================================================

def read_pdf(file):

    try:

        from pypdf import PdfReader

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        # If text found, return it
        if text.strip():
            return text.strip()

        # ==============================
        # OCR FOR SCANNED PDF
        # ==============================

        import pytesseract
        from pdf2image import convert_from_bytes

        # Windows Tesseract path
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        file.seek(0)

        images = convert_from_bytes(file.read())

        ocr_text = ""

        for image in images:

            ocr_text += pytesseract.image_to_string(image)

            ocr_text += "\n"

        return ocr_text.strip()

    except Exception as e:

        raise Exception(f"Unable to read PDF:\n{e}")


# ==========================================================
# READ DOCX
# ==========================================================

def read_docx(file):

    try:

        document = Document(file)

        paragraphs = []

        for para in document.paragraphs:

            if para.text.strip():

                paragraphs.append(para.text)

        return "\n".join(paragraphs)

    except Exception as e:

        raise Exception(f"Unable to read DOCX:\n{e}")


# ==========================================================
# READ TXT
# ==========================================================

def read_txt(file):

    encodings = [

        "utf-8",

        "utf-16",

        "latin-1",

        "cp1252"

    ]

    for encoding in encodings:

        try:

            file.seek(0)

            return file.read().decode(encoding)

        except:

            continue

    raise Exception("Unsupported text encoding.")


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def read_file(uploaded_file):

    if uploaded_file is None:

        return ""

    extension = os.path.splitext(

        uploaded_file.name

    )[1].lower()

    if extension == ".pdf":

        return read_pdf(uploaded_file)

    elif extension == ".docx":

        return read_docx(uploaded_file)

    elif extension == ".txt":

        return read_txt(uploaded_file)

    else:

        raise ValueError(

            "Supported file types are PDF, DOCX and TXT."

        )


# ==========================================================
# FILE INFORMATION
# ==========================================================

def file_info(uploaded_file):

    if uploaded_file is None:

        return {}

    return {

        "name": uploaded_file.name,

        "size_kb": round(uploaded_file.size / 1024, 2),

        "extension": os.path.splitext(

            uploaded_file.name

        )[1].lower()

    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("File Reader Loaded Successfully.")
