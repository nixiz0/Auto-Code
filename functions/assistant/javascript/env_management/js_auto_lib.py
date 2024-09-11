import re


def detect_imports(js_code):
    # Initialize an empty set to store the libraries
    libs = set()
    
    # Regular expressions to find require and import statements
    require_regex = r"require\('([^']+)'\)"
    import_regex = r"import\s+(?:[^'\"\s]+)\s+from\s+'([^']+)'"
    
    # Find All Matches for require
    require_matches = re.findall(require_regex, js_code)
    
    # Find All Matches for import
    import_matches = re.findall(import_regex, js_code)
    
    # Store libraries in a set
    libs.update(require_matches)
    libs.update(import_matches)

    # Check if the set is empty before printing
    if libs:
        print(f"LIB DETECTED: {libs}")
    else:
        print("No libraries detected.")
    
    return libs