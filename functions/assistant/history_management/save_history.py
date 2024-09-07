import streamlit as st
import os
import re
import json
import nltk
import re
from nltk.corpus import stopwords


def create_and_save_history(session_state_updated, selected_file, history_dir, session_name):
    # Check if stopwords for English and French are already downloaded
    try:
        nltk.corpus.stopwords.words('english')
        nltk.corpus.stopwords.words('french')
    except LookupError:
        nltk.download('stopwords')

    stop_words = set(stopwords.words('english')).union(set(stopwords.words('french')))

    # Create file name from user's words and clean the text
    first_user_message = session_state_updated[0]['content']
    cleaned_message = re.sub(r'\W+', ' ', first_user_message).lower()
    cleaned_message = " ".join(word for word in cleaned_message.split() if word not in stop_words)
    history_file_name = " ".join(cleaned_message.split()[:20]) + ".json"

    if 'user' in session_state_updated[0]['role'] and not selected_file:
        history_file_path = os.path.join(history_dir, history_file_name)
    else:
        history_file_path = os.path.join(history_dir, selected_file)

    # Save chat history to a file
    with open(history_file_path, "w", encoding="utf8") as f:
        json.dump(session_state_updated, f, indent=4, ensure_ascii=False)

    # Update selected file
    selected_file = history_file_name

    # Update session_name with 'session_state_updated'
    st.session_state[session_name] = session_state_updated
    st.rerun()

    return selected_file
