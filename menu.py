import streamlit as st
import platform
import os
from streamlit_ace import st_ace

from functions.page_title import set_page_title
from functions.get_model import get_model_names
from functions.assistant.llm import llm_prompt
from functions.assistant.python.py_auto_code_mode import py_auto_code
from functions.assistant.javascript.js_auto_code_mode import js_auto_code
from functions.assistant.history_management.load_history import load_code_history
from functions.assistant.history_management.btn_history import AppButton


# -------- SESSION STATE & HISTORY DECLARATION --------
session_name = 'session_state'
history_dir = "code_history"
if not os.path.exists(history_dir):
    os.makedirs(history_dir)

# Initialize 'session_state' with an empty list for messages
if session_name not in st.session_state:
    st.session_state[session_name] = []

session_state_updated = st.session_state[session_name]

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

# Add a picker to choose a chat history file
history_files = os.listdir(history_dir)
selected_file = st.sidebar.selectbox("Historique de conversation" if lang == 'Fr' else 
                                     "Conversation history file", [""] + history_files, key="selected_file")

if not st.session_state[session_name] == []:
    app_btn = AppButton(lang, history_dir, selected_file, session_name)
    app_btn.rename_file()
    app_btn.download_as_csv()
    app_btn.delete_file()

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

code_lang = ['python', 'javascript', 'sql', 'java', 'html', 'css', 'php', 'c', 'pp', 'csharp', 'vba']
code_language = st.selectbox('Langage Code' if lang == "Fr" else 'Code Language', code_lang)

# -------- AUTO-CODE + PROMPT --------
if not selected_file:
    new_session = st.sidebar.button("Nouveau" if lang == 'Fr' else "New")
    if new_session:
        st.session_state[session_name] = []
        session_state_updated = st.session_state[session_name]
        st.rerun()

    # Text field for prompt
    prompt = st.text_input("Entrez votre prompt:" if lang == 'Fr' else "Enter your prompt:")

    # Initialize the code variable with the latest content
    code = ""

    # Button to generate the code
    if st.button("Générer le code" if lang == 'Fr' else "Generate the code"):
        generated_code = llm_prompt(prompt, lang, model_use, session_state_updated, selected_file, session_name, history_dir)
        st.rerun()

    # Show "RUN" button only if code is generated
    if session_state_updated and session_state_updated[-1]['role'] == 'assistant':
        code = session_state_updated[-1]["content"]

    if code:
        # Use columns for layout
        run_btn, code_editor = st.columns([1, 15])

        with code_editor:
            code = st_ace(value=code, language=code_language, theme='cobalt', height=500)

        if code_language in ['python', 'javascript']:
            with run_btn:
                # Button to run the code
                if st.button("▶️"):
                    if code_language == 'python':
                        output = py_auto_code(code, lang, model_use, session_state_updated, selected_file, session_name, history_dir)
                    elif code_language == 'javascript':
                        output = js_auto_code(code, lang, model_use, session_state_updated, selected_file, session_name, history_dir) 
                    else: 
                        output = "Ce langage de programmation n'est pas pris en compte" if lang == 'Fr' else \
                                "This programming language is not taken into account"
                    st.sidebar.text_area("Terminal Output:", output, height=200)

# -------- LOAD CODE HISTORY --------
if selected_file:
    load_code_history(history_dir, selected_file, session_name, code_language)

# Use the function to set the page title
set_page_title("Menu · Streamlit", "🤖 Auto-Code")