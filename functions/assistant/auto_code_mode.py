import streamlit as st
import shutil
import ast
import os 

from functions.assistant.env_management.create_env import create_virtualenv, install_requirements, run_script
from functions.assistant.llm import llm_prompt


def auto_code(code, lang, model_use, session_state_updated):
    temp_env_path = 'temp_env'
    temp_script_path = 'temp_script.py'
    
    # Check if the folder exists and delete it
    if os.path.exists(temp_env_path) and os.path.isdir(temp_env_path):
        shutil.rmtree(temp_env_path)

    # Check if the file exists and delete it
    if os.path.exists(temp_script_path) and os.path.isfile(temp_script_path):
        os.remove(temp_script_path)

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

    # Parse the code into an AST
    tree = ast.parse(code)

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
    
    result, stdout_output, stderror_output = run_script(env_dir, script_name)
    print(result) # Check the process

    # -------- RECOVER ERROR LOGIC HERE --------   
    if stderror_output == '':
        st.sidebar.success("Ok 😊")
        return f"Script exécuté avec succès:\n{stdout_output}" if lang == 'Fr' else f"Script runs successfully:\n{stdout_output}" 
    else:
        while stderror_output != '':
            st.sidebar.error("Erreur 😑 [Correction automatique en cours...]" if lang == 'Fr' else 
                             "Error 😑 [Auto correction in progress...]")
            
            preprompt = f"Le code ne fonctionne pas j'ai cette erreur, corrige le code:\n{code}\n\n{stderror_output}" if lang == 'Fr' else \
                        f"The code doesn't work I have this error, correct the code:\n{code}\n\n{stderror_output}"
            
            generated_code = llm_prompt(preprompt, lang, model_use, session_state_updated)
            print(f"---------------------------> {generated_code}") # Check the generate LLM Code

            temp_env_path = 'temp_env'
            temp_script_path = 'temp_script.py'
            
            # Check if the folder exists and delete it
            if os.path.exists(temp_env_path) and os.path.isdir(temp_env_path):
                shutil.rmtree(temp_env_path)

            # Check if the file exists and delete it
            if os.path.exists(temp_script_path) and os.path.isfile(temp_script_path):
                os.remove(temp_script_path)

            # Initialize an empty set to store the libraries
            libs = set()
            # Parse the code into an AST
            tree = ast.parse(generated_code)

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
                f.write(generated_code)
            
            result, stdout_output, stderror_output = run_script(env_dir, script_name)
            print(result) # Check the process

            if stderror_output == '':
                st.sidebar.success("Ok 😊")
                return f"Script corrigé avec succès:\n{generated_code}" if lang == 'Fr' else f"Script corrected successfully:\n{generated_code}"
            