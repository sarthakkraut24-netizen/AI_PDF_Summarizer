# ==========================================================
# IMAGE_READER.PY
# AI Document Assistant
# Compatible with Python 3.13+
# ==========================================================

from PIL import Image
from ocr import extract_text_from_image


# ==========================================================
# SUPPORTED IMAGE TYPES
# ==========================================================

SUPPORTED_IMAGES = [

    ".png",

    ".jpg",

    ".jpeg",

    ".bmp",

    ".tiff",

    ".webp"

]


# ==========================================================
# CHECK IMAGE TYPE
# ==========================================================

def is_image(filename):

    filename = filename.lower()

    for extension in SUPPORTED_IMAGES:

        if filename.endswith(extension):

            return True

    return False


# ==========================================================
# READ IMAGE
# ==========================================================

def read_image(uploaded_file):

    try:

        image = Image.open(uploaded_file)

        return image

    except Exception as e:

        raise Exception(

            f"Unable to open image:\n{e}"

        )


# ==========================================================
# IMAGE TO TEXT
# ==========================================================

def image_to_text(uploaded_file):

    try:

        image = read_image(uploaded_file)

        text = extract_text_from_image(image)

        return text.strip()

    except Exception as e:

        raise Exception(

            f"OCR Error:\n{e}"

        )


# ==========================================================
# IMAGE INFORMATION
# ==========================================================

def image_info(uploaded_file):

    image = read_image(uploaded_file)

    return {

        "width": image.width,

        "height": image.height,

        "mode": image.mode,

        "format": image.format

    }


# ==========================================================
# OCR SUCCESS CHECK
# ==========================================================

def has_text(text):

    if text is None:

        return False

    if len(text.strip()) < 5:

        return False

    return True


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def process_image(uploaded_file):

    info = image_info(uploaded_file)

    text = image_to_text(uploaded_file)

    return {

        "text": text,

        "info": info,

        "success": has_text(text)

    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("Image Reader Loaded Successfully.")