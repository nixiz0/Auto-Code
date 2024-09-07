def clean_code(code):
    # Remove Lines Containing Terminal Commands
    cleaned_code = []
    for line in code.split('\n'):
        if not line.strip().startswith(('pip install', 'python -m pip install')):
            cleaned_code.append(line)
    return '\n'.join(cleaned_code)