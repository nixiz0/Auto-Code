import subprocess
import shutil
import os

from functions.assistant.javascript.env_management._js_const_env import *


def install_libraries(libraries):
    temp_dir = os.path.join(TEMP_ENV_PATH)
    os.makedirs(temp_dir, exist_ok=True)
    
    # Vérifiez si npm est installé
    if shutil.which('npm') is None:
        raise EnvironmentError("npm n'est pas installé ou n'est pas dans le PATH.")
    
    # Initialiser un projet Node.js dans le répertoire temporaire
    subprocess.run(['npm', 'init', '-y'], cwd=temp_dir, shell=True)
    
    # Construire la commande npm install avec toutes les librairies
    install_command = ['npm', 'install'] + list(libraries)
    subprocess.run(install_command, cwd=temp_dir, shell=True)
    
    return temp_dir