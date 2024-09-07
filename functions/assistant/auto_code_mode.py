import streamlit as st
import ast
import autopep8

from functions.assistant.env_management.create_env import create_virtualenv, install_requirements, run_script
from functions.assistant.code_management.clean_code import clean_code


def auto_code(code_blocks, lang, model_use):
    # -------- CODE & LIBRAIRIES DETECTION LOGIC HERE --------
    # Extract and print only the code blocks
    for code in code_blocks: 
        st.code(code, language='python')

    if st.button('Run'):
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