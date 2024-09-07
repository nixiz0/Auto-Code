import streamlit as st
import ollama 
import re


def llm_prompt(prompt, lang, model_use, session_state_updated):
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
            code_blocks = re.findall(r'```(?:python)?(.*?)```', response, re.DOTALL)
            for code in code_blocks:
                code = code.strip()
                response = code
            
            # Add model response to message list
            session_state_updated.append({
                "role": "assistant",
                "content": response,
            })

            return response
