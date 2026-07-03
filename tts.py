# ==========================================================
# TTS.PY
# AI Document Assistant
# Compatible with Python 3.13+
# ==========================================================

import os
import tempfile

from gtts import gTTS


# ==========================================================
# SUPPORTED LANGUAGES
# ==========================================================

LANGUAGES = {

    "English": "en",

    "Hindi": "hi",

    "Marathi": "mr",

    "Gujarati": "gu",

    "Punjabi": "pa",

    "Bengali": "bn",

    "Tamil": "ta",

    "Telugu": "te",

    "Kannada": "kn",

    "Malayalam": "ml",

    "Urdu": "ur",

    "French": "fr",

    "German": "de",

    "Spanish": "es",

    "Italian": "it",

    "Portuguese": "pt",

    "Russian": "ru",

    "Japanese": "ja",

    "Korean": "ko",

    "Chinese": "zh-CN",

    "Arabic": "ar"

}


# ==========================================================
# GET LANGUAGE CODE
# ==========================================================

def get_language_code(language):

    return LANGUAGES.get(language, "en")


# ==========================================================
# GET LANGUAGE LIST
# ==========================================================

def get_languages():

    return list(LANGUAGES.keys())


# ==========================================================
# TEXT TO SPEECH
# ==========================================================

def text_to_speech(

    text,

    language="English"

):

    if not text.strip():

        return None

    try:

        language_code = get_language_code(

            language

        )

        tts = gTTS(

            text=text,

            lang=language_code,

            slow=False

        )

        temp_dir = tempfile.gettempdir()

        output_path = os.path.join(

            temp_dir,

            "speech.mp3"

        )

        tts.save(output_path)

        return output_path

    except Exception as e:

        raise Exception(

            f"TTS Error:\n{e}"

        )


# ==========================================================
# SAVE AUDIO
# ==========================================================

def save_audio(

    text,

    filename,

    language="English"

):

    try:

        language_code = get_language_code(

            language

        )

        tts = gTTS(

            text=text,

            lang=language_code,

            slow=False

        )

        tts.save(filename)

        return filename

    except Exception as e:

        raise Exception(

            f"Unable to save audio:\n{e}"

        )


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    sample = """

    Artificial Intelligence
    is transforming the world.

    """

    file = text_to_speech(

        sample,

        "English"

    )

    print(file)