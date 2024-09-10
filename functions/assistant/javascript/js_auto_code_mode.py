import streamlit as st

from functions.assistant.javascript.env_management.js_del_env import del_temp_env_and_script
from functions.assistant.javascript.env_management.js_auto_lib import detect_imports
from functions.assistant.javascript.env_management.js_npm_install import install_libraries
from functions.assistant.javascript.env_management.js_run_script import run_js_script
from functions.assistant.llm import llm_prompt


def js_auto_code(code, lang, model_use, session_state_updated, selected_file, session_name, history_dir):
    del_temp_env_and_script()
    lib = detect_imports(code)
    if lib:
        install_libraries(lib)
    
    result, stdout_output, stderror_output = run_js_script(code)
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
            lib = detect_imports(generated_code)
            if lib:
                install_libraries(lib)
            
            result, stdout_output, stderror_output = run_js_script(code)
            print(result) # Check the process

            if stderror_output == '':
                st.sidebar.success("Ok 😊")
                with open("temp_script.js", "rb") as file:
                    st.sidebar.download_button(
                        label="Télécharger le script corrigé" if lang == 'Fr' else "Download the corrected script",
                        data=file,
                        file_name="temp_script.js",
                        mime="text/x-javascript"
                    )
                return f"Script corrigé avec succès:\n{generated_code}" if lang == 'Fr' else f"Script corrected successfully:\n{generated_code}"
