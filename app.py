# Chatbot with Wikipedia Q&A and translation
import streamlit as st
import wikipedia
from googletrans import Translator

# Language options
LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'te': 'Telugu'
}


GREETINGS = {
    'en': "Hello! Ask me anything.",
    'hi': "नमस्ते! मुझसे कुछ भी पूछें।",
    'te': "హలో! నన్ను ఏదైనా అడగండి."
}

translator = Translator()

def get_wikipedia_answer(question, lang):
    try:
        wikipedia.set_lang(lang)
        search_results = wikipedia.search(question)
        if not search_results:
            return None, []
        # Use the first search result as the most relevant page
        page_title = search_results[0]
        try:
            summary = wikipedia.summary(page_title, sentences=2)
            return summary, []
        except Exception:
            # If summary fails, suggest related topics
            return None, search_results
    except Exception:
        return None, []

def translate_text(text, dest_lang):
    if dest_lang == 'en':
        return text
    try:
        translated = translator.translate(text, dest=dest_lang)
        return translated.text
    except Exception:
        return text

st.title("PolyChat")

# Language selection
lang = st.selectbox("Choose your language:", list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x])


# Display greeting
st.write(GREETINGS[lang])

# Chat input
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


user_input = st.text_input("Ask a question:")


if user_input:
    st.session_state.chat_history.append(("user", user_input))
    # Get answer from Wikipedia in selected language
    wiki_lang = lang if lang in ['en', 'hi', 'te'] else 'en'
    answer, suggestions = get_wikipedia_answer(user_input, wiki_lang)
    if not answer:
        # Try English if not found in selected language
        answer, suggestions = get_wikipedia_answer(user_input, 'en')
        if answer and lang != 'en':
            answer = translate_text(answer, lang)
    elif lang != wiki_lang:
        answer = translate_text(answer, lang)
    if not answer:
        if suggestions:
            suggestion_text = {
                'en': "I couldn't find a direct answer. Did you mean one of these topics?\n- " + "\n- ".join(suggestions),
                'hi': "मुझे सीधा उत्तर नहीं मिला। क्या आप इनमें से किसी विषय के बारे में पूछना चाहेंगे?\n- " + "\n- ".join(suggestions),
                'te': "నాకు ప్రత్యక్ష సమాధానం దొరకలేదు. మీరు వీటిలో ఏదైనా విషయాన్ని అడగాలనుకుంటున్నారా?\n- " + "\n- ".join(suggestions)
            }[lang]
            st.session_state.chat_history.append(("bot", suggestion_text))
        else:
            answer = {
                'en': "Sorry, I couldn't find an answer.",
                'hi': "माफ़ कीजिए, मुझे उत्तर नहीं मिला।",
                'te': "క్షమించండి, నాకు సమాధానం దొరకలేదు."
            }[lang]
            st.session_state.chat_history.append(("bot", answer))
    else:
        st.session_state.chat_history.append(("bot", answer))

# Display chat history
for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Bot:** {msg}")

