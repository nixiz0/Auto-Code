import subprocess
import shutil
import os

from functions.assistant.javascript.env_management._js_const_env import *


def install_libraries(libraries):
    temp_dir = os.path.join(TEMP_ENV_PATH)
    os.makedirs(temp_dir, exist_ok=True)
    
    # Check if npm is installed
    if shutil.which('npm') is None:
        raise EnvironmentError("npm is not installed or is not in the PATH.")
    
    # Initialize a Node.js project in the temporary directory
    subprocess.run(['npm', 'init', '-y'], cwd=temp_dir, shell=True)
    
    # Build the npm install command with all libraries
    install_command = ['npm', 'install'] + list(libraries)
    subprocess.run(install_command, cwd=temp_dir, shell=True)
    
    return temp_dir