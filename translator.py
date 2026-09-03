"""
مترجم متعدد اللغات باستخدام deep-translator
يدعم جميع اللغات بدون API Key
"""
from deep_translator import GoogleTranslator
import streamlit as st

# ذاكرة الترجمة للأداء
translation_cache = {}

def translate_text(text, target_lang='ar', source_lang='auto'):
    """ترجمة النص إلى اللغة المطلوبة"""
    if not text or target_lang == 'en':
        return text

    cache_key = f"{text}_{source_lang}_{target_lang}"
    if cache_key in translation_cache:
        return translation_cache[cache_key]

    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        result = translator.translate(text)
        translation_cache[cache_key] = result
        return result
    except Exception as e:
        return text  # في حالة الفشل، نعيد النص الأصلي

def get_supported_languages():
    """اللغات المدعومة"""
    return {
        'ar': 'العربية',
        'en': 'English',
        'fr': 'Français',
        'es': 'Español',
        'de': 'Deutsch',
        'it': 'Italiano',
        'tr': 'Türkçe',
        'zh': '中文',
        'ja': '日本語',
        'ru': 'Русский'
    }
