from deep_translator import GoogleTranslator

def translate_text(text, dest_language):
    try:
        translation = GoogleTranslator(source='auto', target=dest_language).translate(text)
        print(f"Translated '{text[:50]}...' to '{translation[:50]}...' in {dest_language}")  # Debug
        return translation
    except Exception as e:
        print(f"Error translating text: {e}")
        return None