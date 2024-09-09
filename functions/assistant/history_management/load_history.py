import streamlit as st 
import json
import os


def load_code_history(history_dir, selected_file, session_name):
    # Recover json load file if the user select and load a json
    with open(os.path.join(history_dir, selected_file), "r", encoding="utf8") as f:
        st.session_state['session_state'] = json.load(f)

    # Show all previous posts
    for message in st.session_state[session_name]:
        if message["role"] == "assistant":
            st.code(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.write(message["content"])