import re


def detect_imports(js_code):
    # Initialize an empty set to store the libraries
    libs = set()
    
    # Regular expression to find the require
    regex = r"require\('([^']+)'\)"
    
    # Find All Matches
    matches = re.findall(regex, js_code)
    
    # Store libraries in a set
    libs = set(matches)

    print(f"LIB DETECTED: {libs}")
    
    return libs