import subprocess
import venv
import os
import threading


def create_virtualenv(env_dir):
    venv.create(env_dir, with_pip=True)

def install_requirements(env_dir, libs):
    pip_path = os.path.join(env_dir, 'Scripts', 'pip.exe')
    subprocess.run([pip_path, 'install'] + libs.split())

def run_script(env_dir, script_path):
    python_path = os.path.join(env_dir, 'Scripts', 'python.exe')
    result = subprocess.run([python_path, script_path], capture_output=True, text=True)
    return result
