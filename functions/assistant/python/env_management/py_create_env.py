import subprocess
import venv
import os


def create_virtualenv(env_dir):
    venv.create(env_dir, with_pip=True)

def install_requirements(env_dir, libs):
    pip_path = os.path.join(env_dir, 'Scripts', 'pip.exe')
    subprocess.run([pip_path, 'install'] + libs.split())
