# ==========================================================
# TEXT TO SPEECH
# Compatible with Python 3.13+
# ==========================================================

import os
from gtts import gTTS

# ==========================================================
# OUTPUT DIRECTORY
# ==========================================================

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================================
# LANGUAGE MAP
# ==========================================================

LANGUAGE_CODES = {
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
    "Chinese": "zh-cn",
    "Arabic": "ar",
}

# ==========================================================
# TEXT TO SPEECH
# ==========================================================

def text_to_speech(text, filename="speech.mp3", language="English"):
    """
    Convert text to speech and save as MP3.

    Args:
        text (str): Text to convert.
        filename (str): Output filename.
        language (str): Language name.

    Returns:
        str | None: Path to generated MP3 file.
    """

    if not text or not text.strip():
        return None

    lang = LANGUAGE_CODES.get(language, "en")

    output_path = os.path.join(OUTPUT_DIR, filename)

    try:
        tts = gTTS(
            text=text,
            lang=lang,
            slow=False
        )

        tts.save(output_path)

        return output_path

    except Exception as e:
        print(f"TTS Error: {e}")
        return None


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    file = text_to_speech(
        "Hello! Welcome to AI Document Assistant.",
        filename="test.mp3"
    )

    if file:
        print("Audio saved at:", file)
    else:
        print("Failed to generate speech.")