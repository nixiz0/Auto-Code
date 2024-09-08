import subprocess
import os


def run_script(env_dir, script_path):
    python_path = os.path.join(env_dir, 'Scripts', 'python.exe')
    result = subprocess.run([python_path, script_path], capture_output=True, text=True)
    stdout_output = result.stdout
    stderror_output = result.stderr

    return result, stdout_output, stderror_output