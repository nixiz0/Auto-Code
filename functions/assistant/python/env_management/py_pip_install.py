from functions.assistant.python.env_management.py_create_env import create_virtualenv, install_requirements
from functions.assistant.python.env_management._py_const_env import *


def pip_installer(lib):
    create_virtualenv(TEMP_ENV_PATH)
    if lib != '':
        install_requirements(TEMP_ENV_PATH, lib)