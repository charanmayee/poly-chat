import streamlit as st
import os
from utils.wikipedia_helper import WikipediaHelper
from utils.translation_helper import TranslationHelper
from utils.language_helper import LanguageHelper

# Page configuration
st.set_page_config(
    page_title="PolyChat - Multilingual Chatbot",
    page_icon="🌍",
    layout="wide"
)

# Initialize helpers
@st.cache_resource
def initialize_helpers():
    """Initialize helper classes"""
    return {
        'wikipedia': WikipediaHelper(),
        'translator': TranslationHelper(),
        'language': LanguageHelper()
    }

helpers = initialize_helpers()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'en'

# Language mapping
LANGUAGE_OPTIONS = {
    'English': 'en',
    'Hindi': 'hi',
    'Telugu': 'te'
}

LANGUAGE_NAMES = {
    'en': 'English',
    'hi': 'Hindi',
    'te': 'Telugu'
}

# UI Layout
st.title("🌍 PolyChat - Multilingual Chatbot")
st.markdown("Ask questions in multiple languages and get answers from Wikipedia!")

# Sidebar for language selection
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Language selection
    selected_lang_name = st.selectbox(
        "Select Interface Language:",
        options=list(LANGUAGE_OPTIONS.keys()),
        index=list(LANGUAGE_OPTIONS.values()).index(st.session_state.selected_language)
    )
    
    st.session_state.selected_language = LANGUAGE_OPTIONS[selected_lang_name]
    
    st.markdown("---")
    
    # Chat statistics
    st.subheader("📊 Chat Statistics")
    st.metric("Messages", len(st.session_state.chat_history))
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    
    # Supported languages info
    st.subheader("🗣️ Supported Languages")
    st.markdown("• English")
    st.markdown("• Hindi (हिन्दी)")
    st.markdown("• Telugu (తెలుగు)")

# Main chat interface
col1, col2 = st.columns([3, 1])

with col1:
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history:
            for i, message in enumerate(st.session_state.chat_history):
                if message['type'] == 'user':
                    with st.chat_message("user"):
                        st.write(f"**{message['language']}:** {message['content']}")
                else:
                    with st.chat_message("assistant"):
                        st.write(message['content'])
                        if 'source' in message:
                            st.caption(f"Source: {message['source']}")
        else:
            st.info("👋 Welcome! Ask me anything in English, Hindi, or Telugu!")

    # Input area
    user_input = st.chat_input("Type your question here...")

with col2:
    # Language detection info
    st.subheader("🔍 Language Detection")
    if st.session_state.chat_history:
        last_user_message = None
        for message in reversed(st.session_state.chat_history):
            if message['type'] == 'user':
                last_user_message = message
                break
        
        if last_user_message:
            detected_lang = last_user_message.get('detected_language', 'Unknown')
            confidence = last_user_message.get('confidence', 0)
            st.metric("Detected Language", LANGUAGE_NAMES.get(detected_lang, detected_lang))
            st.metric("Confidence", f"{confidence:.2%}")

# Process user input
if user_input:
    # Detect language of user input
    detected_lang, confidence = helpers['language'].detect_language(user_input)
    
    # Add user message to chat history
    user_message = {
        'type': 'user',
        'content': user_input,
        'language': LANGUAGE_NAMES.get(detected_lang, detected_lang),
        'detected_language': detected_lang,
        'confidence': confidence,
        'timestamp': st.session_state.get('timestamp', 0)
    }
    st.session_state.chat_history.append(user_message)
    
    # Show processing message
    with st.spinner("🔍 Searching Wikipedia and preparing response..."):
        try:
            # Search Wikipedia
            search_results = helpers['wikipedia'].search_wikipedia(user_input, detected_lang)
            
            if search_results:
                # Get the best result
                article_title, article_summary = search_results[0]
                
                # Translate to selected language if different from detected language
                if st.session_state.selected_language != detected_lang:
                    translated_summary = helpers['translator'].translate_text(
                        article_summary, 
                        target_language=st.session_state.selected_language
                    )
                    final_response = translated_summary
                else:
                    final_response = article_summary
                
                # Add assistant response to chat history
                assistant_message = {
                    'type': 'assistant',
                    'content': final_response,
                    'source': f"Wikipedia - {article_title}",
                    'timestamp': st.session_state.get('timestamp', 0) + 1
                }
                st.session_state.chat_history.append(assistant_message)
                
            else:
                # No results found
                no_results_message = "I couldn't find any relevant information on Wikipedia for your question."
                
                # Translate the no results message if needed
                if st.session_state.selected_language != 'en':
                    no_results_message = helpers['translator'].translate_text(
                        no_results_message,
                        target_language=st.session_state.selected_language
                    )
                
                assistant_message = {
                    'type': 'assistant',
                    'content': no_results_message,
                    'timestamp': st.session_state.get('timestamp', 0) + 1
                }
                st.session_state.chat_history.append(assistant_message)
                
        except Exception as e:
            error_message = f"Sorry, I encountered an error while processing your request: {str(e)}"
            
            # Translate error message if needed
            if st.session_state.selected_language != 'en':
                try:
                    error_message = helpers['translator'].translate_text(
                        error_message,
                        target_language=st.session_state.selected_language
                    )
                except:
                    pass  # Keep original error message if translation fails
            
            assistant_message = {
                'type': 'assistant',
                'content': error_message,
                'timestamp': st.session_state.get('timestamp', 0) + 1
            }
            st.session_state.chat_history.append(assistant_message)
    
    # Update timestamp and rerun
    st.session_state.timestamp = st.session_state.get('timestamp', 0) + 2
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    Built with ❤️ using Streamlit, Wikipedia API, and Google Translate
    </div>
    """,
    unsafe_allow_html=True
)
