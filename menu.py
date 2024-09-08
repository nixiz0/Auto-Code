import streamlit as st 
from streamlit_ace import st_ace
import platform
import os 

from functions.page_title import set_page_title
from functions.get_model import get_model_names
from functions.assistant.llm import llm_prompt
from functions.assistant.auto_code_mode import auto_code


# DONT FORGET SESSION STATE UPDATED HAVE ALL THE HISTORY 
# CONVERSATION FOR THE ACTUAL SESSION

# -------- SESSION STATE & HISTORY DECLARATION --------
session_name = 'session_state'

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

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

new_session = st.sidebar.button("Nouveau" if lang == 'Fr' else "New")
if new_session:
    st.session_state[session_name] = []
    session_state_updated = st.session_state[session_name]

# Text field for prompt
prompt = st.text_input("Entrez votre prompt:" if lang == 'Fr' else "Enter your prompt:")

# Initialize the code variable with the latest content
code = ""

# Button to generate the code
if st.button("Générer le code" if lang == 'Fr' else "Generate the code"):
    generated_code = llm_prompt(prompt, lang, model_use, session_state_updated)

# Show "RUN" button only if code is generated
if session_state_updated and session_state_updated[-1]['role'] == 'assistant':
    code = session_state_updated[-1]["content"]

if code != "":
    # Use columns for layout
    run_btn, code_editor = st.columns([1, 15])

    with code_editor:
        code = st_ace(value=code, language='python', theme='cobalt', height=500)

    with run_btn:
        # Button to run the code
        if st.button("▶️"):
            output = auto_code(code, lang, model_use, session_state_updated)
            st.sidebar.text_area("Terminal Output:", output, height=200)

# print(f"\n\n\n\n{session_state_updated}") # Check all the message history during the session

# Use the function to set the page title
set_page_title("Menu · Streamlit", "🤖 Auto-Code")