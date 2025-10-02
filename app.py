import streamlit as st
from langdetect import detect, DetectorFactory
from googletrans import Translator
import os
from datetime import datetime

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Language mapping
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'es': 'Spanish',
    'fr': 'French'
}

LANG_CODE_TO_NAME = {
    'en': 'English',
    'hi': 'Hindi',
    'es': 'Spanish',
    'fr': 'French'
}

# Initialize translator
translator = Translator()


def detect_language(text):
    """
    Detect the language of the input text.
    
    Args:
        text (str): Input text to detect language
        
    Returns:
        str: Language code (e.g., 'en', 'hi', 'es', 'fr')
    """
    try:
        lang = detect(text)
        # Map detected language to supported languages
        if lang in SUPPORTED_LANGUAGES:
            return lang
        # Default to English if language not supported
        return 'en'
    except Exception as e:
        st.error(f"Language detection error: {e}")
        return 'en'


def translate_text(text, source_lang, target_lang):
    """
    Translate text from source language to target language.
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language code
        target_lang (str): Target language code
        
    Returns:
        str: Translated text
    """
    try:
        if source_lang == target_lang:
            return text
        
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return translation.text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text


def generate_response(user_input_english):
    """
    Generate a response based on user input in English.
    Uses rule-based logic with context awareness.
    
    Args:
        user_input_english (str): User input in English
        
    Returns:
        str: Generated response in English
    """
    user_input_lower = user_input_english.lower().strip()
    
    # Greeting responses
    if any(greeting in user_input_lower for greeting in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! I'm PolyChat, your multilingual companion. How can I help you today?"
    
    # Farewell responses
    elif any(farewell in user_input_lower for farewell in ['bye', 'goodbye', 'see you', 'farewell']):
        return "Goodbye! It was nice talking to you. Feel free to come back anytime!"
    
    # How are you
    elif any(phrase in user_input_lower for phrase in ['how are you', 'how do you do', 'how are things']):
        return "I'm doing great, thank you for asking! I'm here to chat with you in multiple languages. How are you doing?"
    
    # Name queries
    elif any(phrase in user_input_lower for phrase in ['what is your name', 'who are you', 'your name']):
        return "I'm PolyChat, a multilingual chatbot that can communicate in English, Hindi, Spanish, and French!"
    
    # Help queries
    elif any(phrase in user_input_lower for phrase in ['help', 'what can you do', 'capabilities']):
        return "I can chat with you in English, Hindi, Spanish, and French. I automatically detect your language and respond accordingly. Just type your message and I'll understand!"
    
    # Language queries
    elif any(phrase in user_input_lower for phrase in ['what languages', 'which languages', 'languages support']):
        return "I support English, Hindi, Spanish, and French. You can type in any of these languages and I'll understand!"
    
    # Thank you
    elif any(phrase in user_input_lower for phrase in ['thank you', 'thanks', 'appreciate']):
        return "You're very welcome! I'm happy to help. Is there anything else you'd like to know?"
    
    # Time queries
    elif any(phrase in user_input_lower for phrase in ['what time', 'current time', 'time is it']):
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."
    
    # Date queries
    elif any(phrase in user_input_lower for phrase in ['what date', 'today date', 'what day']):
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}."
    
    # Weather (simulated)
    elif 'weather' in user_input_lower:
        return "I don't have access to real-time weather data, but I hope it's nice where you are! You might want to check a weather service for accurate information."
    
    # Joke
    elif 'joke' in user_input_lower:
        return "Why don't scientists trust atoms? Because they make up everything! 😄"
    
    # General conversation
    else:
        # Context-aware responses based on conversation history
        if len(st.session_state.messages) > 2:
            return "That's interesting! Tell me more about that, or feel free to ask me anything else."
        else:
            return "I understand. I'm here to chat with you in multiple languages. What would you like to talk about?"


def initialize_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'language_override' not in st.session_state:
        st.session_state.language_override = 'Auto-detect'


def main():
    """Main Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="PolyChat - Multilingual Chatbot",
        page_icon="🌍",
        layout="centered"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Custom CSS for better UI
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: #4CAF50;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
        }
        .user-message {
            background-color: #E3F2FD;
            margin-left: 2rem;
        }
        .bot-message {
            background-color: #F1F8E9;
            margin-right: 2rem;
        }
        .message-label {
            font-weight: bold;
            margin-bottom: 0.3rem;
        }
        .language-badge {
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 5px;
            background-color: #FFF3E0;
            color: #E65100;
            font-size: 0.8rem;
            margin-top: 0.3rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">🌍 PolyChat</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your Multilingual Companion</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Language override dropdown
        st.subheader("Language Settings")
        language_options = ['Auto-detect'] + list(SUPPORTED_LANGUAGES.values())
        st.session_state.language_override = st.selectbox(
            "Override Language Detection:",
            language_options,
            index=0
        )
        
        st.markdown("---")
        
        # Clear conversation button
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Information
        st.subheader("ℹ️ About")
        st.markdown("""
        **PolyChat** is a multilingual chatbot that supports:
        - 🇬🇧 English
        - 🇮🇳 Hindi
        - 🇪🇸 Spanish
        - 🇫🇷 French
        
        Simply type your message in any supported language, and PolyChat will respond in the same language!
        """)
        
        st.markdown("---")
        st.caption("Built with Streamlit 💙")
    
    # Display chat messages
    for message in st.session_state.messages:
        message_class = "user-message" if message["role"] == "user" else "bot-message"
        with st.container():
            st.markdown(f'<div class="chat-message {message_class}">', unsafe_allow_html=True)
            role_emoji = "👤" if message["role"] == "user" else "🤖"
            st.markdown(f'<div class="message-label">{role_emoji} {message["role"].title()}</div>', unsafe_allow_html=True)
            st.write(message["content"])
            if "language" in message:
                lang_name = LANG_CODE_TO_NAME.get(message["language"], message["language"])
                st.markdown(f'<span class="language-badge">🌐 {lang_name}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Determine language
        if st.session_state.language_override == 'Auto-detect':
            detected_lang = detect_language(user_input)
        else:
            # Reverse lookup: language name to code
            lang_code_map = {v: k for k, v in SUPPORTED_LANGUAGES.items()}
            detected_lang = lang_code_map.get(st.session_state.language_override, 'en')
        
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "language": detected_lang
        })
        
        # Translate to English if needed
        if detected_lang != 'en':
            user_input_english = translate_text(user_input, detected_lang, 'en')
        else:
            user_input_english = user_input
        
        # Generate response in English
        response_english = generate_response(user_input_english)
        
        # Translate response back to user's language
        if detected_lang != 'en':
            response = translate_text(response_english, 'en', detected_lang)
        else:
            response = response_english
        
        # Add bot response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "language": detected_lang
        })
        
        # Rerun to display new messages
        st.rerun()
    
    # Show a welcome message if no messages
    if len(st.session_state.messages) == 0:
        st.info("👋 Welcome to PolyChat! Start chatting in English, Hindi, Spanish, or French!")


if __name__ == "__main__":
    main()
