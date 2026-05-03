import glob
import re

html_files = glob.glob('templates/*.html')

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Remove the background-color rule from the overscroll fix
    content = content.replace("background-color: #09090b; /* Fallback for dark mode rubber band */", "")
    
    with open(filepath, 'w') as file:
        file.write(content)

print("Canvas visibility fixed")
