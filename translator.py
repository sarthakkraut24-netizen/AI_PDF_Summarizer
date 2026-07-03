# ==========================================================
# TRANSLATOR.PY
# AI Document Assistant
# Compatible with Python 3.13+
# ==========================================================

from deep_translator import GoogleTranslator

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
# GET LANGUAGE LIST
# ==========================================================

def get_languages():
    return list(LANGUAGES.keys())

# ==========================================================
# GET LANGUAGE CODE
# ==========================================================

def get_language_code(language):
    return LANGUAGES.get(language, "en")

# ==========================================================
# TRANSLATE TEXT
# ==========================================================

def translate_text(text, target_language="English"):

    if not text.strip():
        return ""

    try:

        language_code = get_language_code(target_language)

        translated = GoogleTranslator(
            source="auto",
            target=language_code
        ).translate(text)

        return translated

    except Exception as e:

        raise Exception(
            f"Translation Error:\n{e}"
        )

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    sample = "Artificial Intelligence is changing the world."

    print(
        translate_text(
            sample,
            "Hindi"
        )
    )