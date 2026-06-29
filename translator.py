# ==========================================================
# TRANSLATOR
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
# TRANSLATE TEXT
# ==========================================================

def translate_text(text, language="English"):

    if not text.strip():
        return ""

    if language == "English":
        return text

    try:

        translator = GoogleTranslator(
            source="auto",
            target=LANGUAGES.get(language, "en")
        )

        translated = translator.translate(text)

        return translated

    except Exception as e:

        return f"Translation Error: {e}"


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
# TEST
# ==========================================================

if __name__ == "__main__":

    sample = """
    Artificial Intelligence is transforming the world.
    """

    print("Original:\n")
    print(sample)

    print("\nHindi:\n")
    print(translate_text(sample, "Hindi"))

    print("\nMarathi:\n")
    print(translate_text(sample, "Marathi"))