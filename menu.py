import streamlit as st 
import platform
import os 

from functions.page_title import set_page_title
from functions.get_model import get_model_names
from functions.assistant.llm import llm_prompt


# -------- SESSION STATE & HISTORY DECLARATION --------
session_name = 'session_state'
history_dir = "conversation_history"
if not os.path.exists(history_dir):
    os.makedirs(history_dir)

# -------- SIDEBAR --------
lang_col, params_model_col = st.sidebar.columns([3,1], vertical_alignment='bottom')

with lang_col:
    lang = st.selectbox('🔤 Language', ['Fr', 'En'])

with params_model_col:
    # Add a button to the sidebar that redirects to modelfile.py
    if st.button('🛠️' if lang == 'Fr' else '🛠️'):
        if platform.system() == "Windows":
            os.system("start cmd /K python functions/prompt_engineering/modelfile.py")
        else:
            os.system("gnome-terminal -e 'bash -c \"python functions/prompt_engineering/modelfile.py; exec bash\"'")

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

model_names = get_model_names()
model_names.insert(0, "")
model_use = st.sidebar.selectbox('🔬 Modèles' if lang == "Fr" else '🔬 Models', model_names)

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

# Add a picker to choose a chat history file
history_files = os.listdir(history_dir)
selected_file = st.sidebar.selectbox("Historique de conversation" if lang == 'Fr' else 
                                     "Conversation history file", [""] + history_files)

# Initialize 'session_state' with an empty list for messages
if session_name not in st.session_state:
    st.session_state[session_name] = []

session_state_updated = st.session_state[session_name]

# -------- QUESTION & AUTO-CODE LOGIC HERE --------
prompt = st.chat_input("Posez une question" if lang == 'Fr' else "Ask a Question")

llm_prompt(prompt, lang, model_use, session_state_updated, selected_file, history_dir, session_name)

# Show all previous posts
for message in st.session_state[session_name]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Use the function to set the page title
set_page_title("Menu · Streamlit", "🤖 Auto-Code")