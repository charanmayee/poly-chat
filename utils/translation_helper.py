import streamlit as st
from deep_translator import GoogleTranslator
from typing import Optional

class TranslationHelper:
    """Helper class for translation operations"""
    
    def __init__(self):
        """Initialize translation helper"""
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'te': 'Telugu'
        }
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'auto') -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (auto-detect if 'auto')
            
        Returns:
            Translated text
        """
        try:
            if not text or not text.strip():
                return text
            
            # Don't translate if target and source are the same
            if source_language == target_language:
                return text
            
            # Perform translation using deep-translator
            translator = GoogleTranslator(source=source_language, target=target_language)
            result = translator.translate(text)
            
            return result
            
        except Exception as e:
            st.error(f"Translation error: {str(e)}")
            # Return original text if translation fails
            return text
    
    
    def is_supported_language(self, language_code: str) -> bool:
        """
        Check if language is supported
        
        Args:
            language_code: Language code to check
            
        Returns:
            True if supported, False otherwise
        """
        return language_code in self.supported_languages
    
    def translate_to_all_supported(self, text: str, source_language: str = 'auto') -> dict:
        """
        Translate text to all supported languages
        
        Args:
            text: Text to translate
            source_language: Source language code
            
        Returns:
            Dictionary with language codes as keys and translations as values
        """
        translations = {}
        
        for lang_code in self.supported_languages.keys():
            if lang_code != source_language:
                translations[lang_code] = self.translate_text(text, lang_code, source_language)
            else:
                translations[lang_code] = text
        
        return translations
