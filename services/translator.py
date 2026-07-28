# app/services/translator.py

from deep_translator import GoogleTranslator


def translate_text(text: str):

    if not text:
        return None

    try:
        translated = GoogleTranslator(
            source="ka",
            target="en"
        ).translate(text)

        return translated

    except Exception as e:
        print("Translation error:", e)
        return text