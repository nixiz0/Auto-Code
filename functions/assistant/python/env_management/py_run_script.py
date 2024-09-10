import subprocess
import os


def run_script(code, env_dir, script_path):
    with open("temp_script.py", "w", encoding='utf-8') as f:
        f.write(code)

    # Vérifie si l'environnement virtuel existe
    if os.path.exists(env_dir):
        python_path = os.path.join(env_dir, 'Scripts', 'python.exe')
    else:
        python_path = 'python'
    
    result = subprocess.run([python_path, script_path], capture_output=True, text=True)
    stdout_output = result.stdout
    stderror_output = result.stderr

    return result, stdout_output, stderror_output