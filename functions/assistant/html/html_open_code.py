import webbrowser
import os


def website_open(code):
    filename = 'temp_html.html'
    
    # Check if the file already exists
    if os.path.exists(filename):
        os.remove(filename)
    
    # Create and write to the new file
    with open(filename, 'w') as file:
        file.write(code)
    
    # Get the absolute path of the file
    file_path = os.path.abspath(filename)
    
    # Open the HTML file in the default browser
    webbrowser.open(f'file://{file_path}')