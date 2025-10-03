import streamlit as st
from langdetect import detect, detect_langs
from langdetect.lang_detect_exception import LangDetectException
from typing import Tuple, Optional

class LanguageHelper:
    """Helper class for language detection and management"""
    
    def __init__(self):
        """Initialize language helper"""
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi', 
            'te': 'Telugu'
        }
        
        # Language name mappings
        self.language_names = {
            'en': 'English',
            'hi': 'Hindi',
            'te': 'Telugu'
        }
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect language of given text with confidence score
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (language_code, confidence_score)
        """
        try:
            if not text or not text.strip():
                return 'en', 0.0
            
            # Use langdetect for detection
            detection_results = detect_langs(text)
            
            if detection_results:
                # Get the most probable language
                best_result = detection_results[0]
                detected_lang = best_result.lang
                confidence = best_result.prob
                
                # Map some common language variants
                lang_mapping = {
                    'hi': 'hi',  # Hindi
                    'te': 'te',  # Telugu
                    'en': 'en',  # English
                    'ta': 'te',  # Tamil mapped to Telugu (fallback)
                    'ur': 'hi',  # Urdu mapped to Hindi (fallback)
                }
                
                detected_lang = lang_mapping.get(detected_lang, detected_lang)
                
                # If detected language is not in our supported list, default to English
                if detected_lang not in self.supported_languages:
                    detected_lang = 'en'
                    confidence = 0.5  # Lower confidence for fallback
                
                return detected_lang, confidence
            
            return 'en', 0.0
            
        except LangDetectException as e:
            # Fallback to English if detection fails
            return 'en', 0.0
            
        except Exception as e:
            st.error(f"Language detection error: {str(e)}")
            return 'en', 0.0
    
    def is_supported_language(self, language_code: str) -> bool:
        """
        Check if language is supported by the application
        
        Args:
            language_code: Language code to check
            
        Returns:
            True if supported, False otherwise
        """
        return language_code in self.supported_languages
    
    def get_language_name(self, language_code: str) -> str:
        """
        Get human-readable name for language code
        
        Args:
            language_code: Language code
            
        Returns:
            Human-readable language name
        """
        return self.language_names.get(language_code, language_code.upper())
    
    def get_supported_languages(self) -> dict:
        """
        Get all supported languages
        
        Returns:
            Dictionary of language codes and names
        """
        return self.supported_languages.copy()
    
    def validate_text_language(self, text: str, expected_language: Optional[str] = None) -> bool:
        """
        Validate if text matches expected language
        
        Args:
            text: Text to validate
            expected_language: Expected language code
            
        Returns:
            True if text matches expected language or if no expectation
        """
        try:
            if not expected_language:
                return True
            
            detected_lang, confidence = self.detect_language(text)
            
            # Accept if confidence is reasonable and language matches
            return detected_lang == expected_language and confidence > 0.3
            
        except Exception:
            return True  # Be permissive on errors
    
    def get_text_statistics(self, text: str) -> dict:
        """
        Get various statistics about the text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with text statistics
        """
        try:
            detected_lang, confidence = self.detect_language(text)
            
            stats = {
                'character_count': len(text),
                'word_count': len(text.split()),
                'detected_language': detected_lang,
                'language_name': self.get_language_name(detected_lang),
                'confidence': confidence,
                'is_supported': self.is_supported_language(detected_lang)
            }
            
            return stats
            
        except Exception as e:
            return {
                'character_count': len(text) if text else 0,
                'word_count': len(text.split()) if text else 0,
                'detected_language': 'unknown',
                'language_name': 'Unknown',
                'confidence': 0.0,
                'is_supported': False,
                'error': str(e)
            }
