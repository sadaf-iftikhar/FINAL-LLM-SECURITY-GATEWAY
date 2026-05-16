from langdetect import detect, LangDetectException

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return lang
    except LangDetectException:
        return "en"

def get_language_name(code: str) -> str:
    names = {
        "en": "English",
        "ur": "Urdu",
        "ko": "Korean",
        "ar": "Arabic",
        "hi": "Hindi"
    }
    return names.get(code, "Unknown")