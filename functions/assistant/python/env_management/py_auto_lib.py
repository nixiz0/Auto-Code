import ast


def auto_lib_detect(code, already_in_python, module_to_pip):
    # Initialize an empty set to store the libraries
    libs = set()

    try:
        # Try to parse the code into an AST
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"Syntax Code Error detected: {e}")
        
        # Return an empty string if there is a syntax error
        return ""

    # Traverse the AST to find import statements
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name.split('.')[0]
                if module_name not in already_in_python:
                    libs.add(module_to_pip.get(module_name, module_name))
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module.split('.')[0]
            if module_name not in already_in_python:
                libs.add(module_to_pip.get(module_name, module_name))

    # Convert the set to a space-separated string
    lib = ' '.join(libs)
    print(f"LIB DETECTED: {lib}")  # Check if the libs are recovered

    return lib