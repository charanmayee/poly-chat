# PolyChat - Multilingual Chatbot

## Overview

PolyChat is a multilingual chatbot application built with Streamlit that enables users to ask questions in multiple languages (English, Hindi, Telugu) and retrieve answers from Wikipedia. The application features automatic language detection, translation capabilities, and multilingual Wikipedia search functionality.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
**Framework**: Streamlit web application framework
- **Rationale**: Streamlit provides rapid development of data-focused web applications with minimal frontend code
- **Session Management**: Uses Streamlit's built-in session state for managing chat history and language preferences
- **Caching**: Implements `@st.cache_resource` decorator for helper class initialization to improve performance
- **Layout**: Wide layout configuration for better content presentation

### Backend Architecture
**Modular Helper Pattern**: The application uses a helper-based architecture with three core modules:

1. **WikipediaHelper** (`utils/wikipedia_helper.py`)
   - Handles Wikipedia API interactions
   - Supports multi-language Wikipedia searches (English, Hindi, Telugu)
   - Implements error handling for disambiguation pages
   - Returns article titles and summaries (limited to 3 sentences per article)

2. **TranslationHelper** (`utils/translation_helper.py`)
   - Manages text translation between supported languages
   - Uses Google Translate API via `deep-translator` library (GoogleTranslator)
   - Supports automatic source language detection
   - Includes fallback mechanism to return original text on translation failures
   - **Updated (Oct 2025)**: Migrated from googletrans to deep-translator for Python 3.13 compatibility

3. **LanguageHelper** (`utils/language_helper.py`)
   - Performs language detection using `langdetect` library
   - Returns language codes with confidence scores
   - Maps language variants to supported language codes
   - Handles edge cases like empty text input

**Design Pattern**: Separation of concerns through distinct helper classes, each responsible for a specific domain (Wikipedia, translation, language detection)

**Alternatives Considered**: Monolithic approach with all logic in app.py
- **Pros of chosen approach**: Better code organization, testability, and maintainability
- **Cons**: Slightly more complex file structure for a small application

### Language Support
**Supported Languages**: English (en), Hindi (hi), Telugu (te)
- Language codes follow ISO 639-1 standard
- Consistent mapping across all helper modules
- Bidirectional translation support between all language pairs

### State Management
**Session State Variables**:
- `chat_history`: Stores conversation history as a list
- `selected_language`: Tracks user's current language preference

**Rationale**: Streamlit's session state provides persistent storage across reruns without requiring external state management solutions

## External Dependencies

### Third-Party Libraries
1. **streamlit**: Web application framework for the user interface
2. **wikipedia**: Python wrapper for Wikipedia API
   - Provides search and summary retrieval functionality
   - Supports multiple language Wikipedias
3. **deep-translator**: Translation library with support for multiple translation engines
   - Enables text translation between languages using Google Translate API
   - More actively maintained and Python 3.13 compatible than googletrans
   - Version: 1.11.4
4. **langdetect**: Language detection library
   - Port of Google's language-detection library
   - Returns language codes with probability scores

### External APIs
1. **Wikipedia API**: Accessed through the `wikipedia` Python library
   - Used for searching articles and retrieving summaries
   - Language-specific Wikipedia instances (en.wikipedia.org, hi.wikipedia.org, te.wikipedia.org)
2. **Google Translate**: Accessed through `deep-translator` library
   - Uses GoogleTranslator for translation operations
   - More reliable and Python 3.13 compatible than the older googletrans library

### Potential Issues
- **Rate Limiting**: Both Wikipedia and Google Translate may impose rate limits on excessive requests
- **Alternative Consideration**: Official translation APIs (Google Cloud Translation API, Azure Translator) would provide more reliability but require API keys and billing setup
