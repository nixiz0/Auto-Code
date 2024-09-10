import streamlit as st

from functions.assistant.python.env_management._py_const_env import *
from functions.assistant.python.env_management.py_del_env import del_temp_env_and_script
from functions.assistant.python.env_management.py_auto_lib import auto_lib_detect
from functions.assistant.python.env_management.py_pip_install import pip_installer
from functions.assistant.python.env_management.py_run_script import run_script
from functions.assistant.llm import llm_prompt


def py_auto_code(code, lang, model_use, session_state_updated, selected_file, session_name, history_dir):
    del_temp_env_and_script()
    lib = auto_lib_detect(code, ALREADY_IN_PYTHON, MODULE_TO_PIP)
    pip_installer(lib, code)
    
    result, stdout_output, stderror_output = run_script(TEMP_ENV_PATH, TEMP_SCRIPT_PATH)
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
            
            generated_code = llm_prompt(preprompt, lang, model_use, session_state_updated, selected_file, session_name, history_dir)
            print(f"---------------------------> {generated_code}") # Check the generate LLM Code

            del_temp_env_and_script()
            lib = auto_lib_detect(generated_code, ALREADY_IN_PYTHON, MODULE_TO_PIP)
            pip_installer(lib, generated_code)
            
            result, stdout_output, stderror_output = run_script(TEMP_ENV_PATH, TEMP_SCRIPT_PATH)
            print(result) # Check the process

            if stderror_output == '':
                st.sidebar.success("Ok 😊")
                with open("temp_script.py", "rb") as file:
                    st.sidebar.download_button(
                        label="Télécharger le script corrigé" if lang == 'Fr' else "Download the corrected script",
                        data=file,
                        file_name="temp_script.py",
                        mime="text/x-python"
                    )
                return f"Script corrigé avec succès:\n{generated_code}" if lang == 'Fr' else f"Script corrected successfully:\n{generated_code}"
