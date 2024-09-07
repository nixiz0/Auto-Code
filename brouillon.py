import streamlit as st
import ollama 
import json
import os
import re
import ast
import autopep8

from functions.assistant.history_management.save_history import create_and_save_history
from functions.assistant.history_management.app_button import AppButton
from functions.assistant.env_management.create_env import create_virtualenv, install_requirements, run_script
from functions.assistant.code_management.clean_code import clean_code


def auto_code(prompt, lang, model_use, session_state_updated, selected_file, history_dir, session_name):
    app_btn = AppButton(lang, history_dir, selected_file, session_name)
    # Recover json load file if the user select and load a json
    if selected_file:
        with open(os.path.join(history_dir, selected_file), "r", encoding="utf8") as f:
            st.session_state['session_state'] = json.load(f)

        app_btn.rename_file()   
        app_btn.download_as_csv() 
        app_btn.delete_file()

    if not selected_file:
        app_btn.new_file()

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
            
            # Add model response to message list
            session_state_updated.append({
                "role": "assistant",
                "content": response,
            })

        # -------- CODE & LIBRAIRIES DETECTION LOGIC HERE --------
        # Extract and print only the code blocks
        code_blocks = re.findall(r'```(?:python)?(.*?)```', response, re.DOTALL)
        for code in code_blocks:
            code = code.strip()
            code = clean_code(code)
            print(code) # Check if the code is recover

            try:
                # Parse the code into an AST
                tree = ast.parse(code)
            except IndentationError:
                # If there's an indentation error, fix the code using autopep8
                code = autopep8.fix_code(code)

                # Try parsing the fixed code again
                tree = ast.parse(code)

            # Initialize an empty set to store the libraries
            libs = set()

            # List of Python Standard Modules
            already_in_python = {
                'time', 'os', 'subprocess', 'shutil', 'sys', 'math', 'json', 're', 
                'datetime', 'itertools', 'functools', 'collections', 'random', 'string', 
                'pathlib', 'logging', 'tkinter', 
            }

            module_to_pip = {
                'BeautifulSoup': 'beautifulsoup4',
                'beautifulsoup': 'beautifulsoup4',
                'bs4': 'beautifulsoup4',
                'bsp': 'beautifulsoup4',
                'PIL': 'Pillow',
                'sklearn': 'scikit-learn',
                'cv2': 'opencv-python',
            }

            # Traverse the AST to find import statements
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name.split('.')[0]
                        if module_name not in already_in_python:
                            libs.add(module_to_pip.get(module_name, module_name))
                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module.split('.')[0]
                    if module_name not in already_in_python:
                        libs.add(module_to_pip.get(module_name, module_name))

            # Convert the set to a space-separated string
            lib = ' '.join(libs)
            print(f"LIB DETECTED: {lib}") # Check if the lib are recover

            # -------- CREATE & RUN TEMP ENV LOGIC HERE --------
            env_dir = "temp_env"
            script_name = "temp_script.py"
            create_virtualenv(env_dir)
            if lib != '':
                install_requirements(env_dir, lib)
            
            with open("temp_script.py", "w", encoding='utf-8') as f:
                f.write(code)
            
            result = run_script(env_dir, script_name)
            # print(result) # Check the process

            # -------- RECOVER ERROR LOGIC HERE --------
            code_error = result.stderr
            print(code_error) # Display the error

            # -------- AUTO-CODE CORRECTION LOGIC HERE --------
            while code_error != '':
                if lang == 'Fr':
                    preprompt = f"Le code fourni ne fonctionne pas, corrige le code et donne tout le code corrigé : {code_error}"
                else: 
                    preprompt = f"The code provided does not work, fixes the code and gives all the corrected code : {code_error}"
                    
                # Add user's message to message list
                session_state_updated.append({
                    "role": "user",
                    "content": preprompt,
                })
                
                # Push the user prompt in the LLM model and return response
                with st.spinner("Réflexion.." if lang == 'Fr' else "Thinking.."):
                    result = ollama.chat(model=model_use, messages=session_state_updated)
                    response = result["message"]["content"]
                    
                    # Add model response to message list
                    session_state_updated.append({
                        "role": "assistant",
                        "content": response,
                    })

                # Extract and print only the code blocks
                code_blocks = re.findall(r'```(?:python)?(.*?)```', response, re.DOTALL)
                for code in code_blocks:
                    code = code.strip()
                    code = clean_code(code)
                    # print(code) # Check if the code is recover

                    try:
                        # Parse the code into an AST
                        tree = ast.parse(code)
                    except IndentationError:
                        # If there's an indentation error, fix the code using autopep8
                        code = autopep8.fix_code(code)

                        # Try parsing the fixed code again
                        tree = ast.parse(code)

                    # Initialize an empty set to store the libraries
                    libs = set()

                    # Traverse the AST to find import statements
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                module_name = alias.name.split('.')[0]
                                if module_name not in already_in_python:
                                    libs.add(module_to_pip.get(module_name, module_name))
                        elif isinstance(node, ast.ImportFrom):
                            module_name = node.module.split('.')[0]
                            if module_name not in already_in_python:
                                libs.add(module_to_pip.get(module_name, module_name))

                    # Convert the set to a space-separated string
                    lib = ' '.join(libs)
                    print(f"LIB DETECTED: {lib}") # Check if the lib are recover

                    if lib != '':
                        install_requirements(env_dir, lib)

                    with open("temp_script.py", "w", encoding='utf-8') as f:
                        f.write(code)

                    result = run_script(env_dir, script_name)
                    code_error = result.stderr
                    print(code_error) # Display the error

                    # Save in new json file if first prompt or an already existing json and add updated prompt
                    selected_file = create_and_save_history(session_state_updated, selected_file, history_dir, session_name)

            # -------- GIVE FINAL CODE LOGIC HERE --------


        # Show all previous posts
        for message in st.session_state[session_name]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Save in new json file if first prompt or an already existing json and add updated prompt
        selected_file = create_and_save_history(session_state_updated, selected_file, history_dir, session_name)

        return session_state_updated
