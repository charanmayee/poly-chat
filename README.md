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
   - Uses Google Translate API via `googletrans` library
   - Supports automatic source language detection
   - Includes fallback mechanism to return original text on translation failures

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
3. **googletrans**: Unofficial Google Translate API client
   - Enables text translation between languages
   - Note: May have rate limiting or reliability concerns as an unofficial API
4. **langdetect**: Language detection library
   - Port of Google's language-detection library
   - Returns language codes with probability scores

### External APIs
1. **Wikipedia API**: Accessed through the `wikipedia` Python library
   - Used for searching articles and retrieving summaries
   - Language-specific Wikipedia instances (en.wikipedia.org, hi.wikipedia.org, te.wikipedia.org)
2. **Google Translate**: Accessed through `googletrans` library
   - Unofficial API wrapper (potential stability concerns)
   - Used for all translation operations

### Potential Issues
- **googletrans**: Being an unofficial API wrapper, it may break if Google changes their translation service
- **Rate Limiting**: Both Wikipedia and Google Translate may impose rate limits on excessive requests
- **Alternative Consideration**: Official translation APIs (Google Cloud Translation API, Azure Translator) would provide more reliability but require API keys and billing setup
