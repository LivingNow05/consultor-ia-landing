import glob
import re

html_files = glob.glob('templates/*.html')

new_fonts = """    <!-- Fonts: Google Sans (Headers) + Inter (Body) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="https://fonts.cdnfonts.com/css/google-sans" rel="stylesheet">
"""

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Replace the old Google Fonts link
    content = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?family=Outfit.*?rel="stylesheet">', new_fonts, content, flags=re.DOTALL)
    
    # Update the Tailwind CSS variables mapping in the <style> block
    # We need to change font-family: 'Outfit', ... to 'Google Sans', ...
    content = content.replace("font-family: 'Outfit', sans-serif;", "font-family: 'Google Sans', sans-serif;")
    content = content.replace("font-family: 'Manrope', sans-serif;", "font-family: 'Inter', sans-serif;")
    
    with open(filepath, 'w') as file:
        file.write(content)

print("Fonts updated to Google Sans + Inter")
