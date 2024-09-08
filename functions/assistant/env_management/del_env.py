import shutil
import os
from functions.assistant.env_management._const_env import *


def del_temp_env_and_script():
    # Check if the folder exists and delete it
    if os.path.exists(TEMP_ENV_PATH) and os.path.isdir(TEMP_ENV_PATH):
        shutil.rmtree(TEMP_ENV_PATH)

    # Check if the file exists and delete it
    if os.path.exists(TEMP_SCRIPT_PATH) and os.path.isfile(TEMP_SCRIPT_PATH):
        os.remove(TEMP_SCRIPT_PATH)