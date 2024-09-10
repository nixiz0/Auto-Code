import subprocess
import os

from functions.assistant.javascript.env_management._js_const_env import *


def run_js_script(code):
    if not os.path.exists(TEMP_ENV_PATH):
        os.makedirs(TEMP_ENV_PATH)
    
    script_dir = os.path.dirname(TEMP_SCRIPT_PATH)
    if script_dir and not os.path.exists(script_dir):
        os.makedirs(script_dir)

    with open(TEMP_SCRIPT_PATH, "w", encoding='utf-8') as f:
        f.write(code)

    node_path = 'node'
    
    env = os.environ.copy()
    env['NODE_PATH'] = os.path.join(TEMP_ENV_PATH, 'node_modules')

    result = subprocess.run([node_path, TEMP_SCRIPT_PATH], capture_output=True, text=True, shell=True, env=env)
    stdout_output = result.stdout
    stderror_output = result.stderr

    return result, stdout_output, stderror_output