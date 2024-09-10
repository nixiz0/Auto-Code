import re


def detect_imports(js_code):
    # Initialize an empty set to store the libraries
    libs = set()
    
    # Expression régulière pour trouver les require
    regex = r"require\('([^']+)'\)"
    
    # Trouver toutes les correspondances
    matches = re.findall(regex, js_code)
    
    # Stocker les librairies dans un ensemble
    libs = set(matches)

    print(f"LIB DETECTED: {libs}")  # Check if the libs are recovered
    
    return libs