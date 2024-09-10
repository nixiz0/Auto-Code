import streamlit as st
import ollama 
import re

from functions.assistant.history_management.save_history import create_and_save_history


def llm_prompt(prompt, lang, model_use, session_state_updated, selected_file, session_name, history_dir):
    if prompt:
        # Add user's message to message list
        session_state_updated.append({
            "role": "user",
            "content": prompt,
        })
        
        # Push the user prompt in the LLM model and return response
        with st.spinner("Réflexion.." if lang == 'Fr' else "Thinking.."):
            result = ollama.chat(model=model_use, messages=session_state_updated)
            response = result["message"]["content"]
            # print(response) # Check the entire response of the LLM

            # Extract and print only the code blocks
            code_blocks = re.findall(r'```(?:python|javascript|html)?(.*?)```', response, re.DOTALL)
            for code in code_blocks:
                code = code.strip()
                response = code
            
            # Add model response to message list
            session_state_updated.append({
                "role": "assistant",
                "content": response,
            })

            # Save in new json file if first prompt or an already existing json and add updated prompt
            selected_file = create_and_save_history(session_state_updated, selected_file, history_dir, session_name)

            return response
