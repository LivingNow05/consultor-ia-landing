import glob
import re

html_files = glob.glob('templates/*.html')

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # 1. Fix Tailwind Config
    content = re.sub(r'body:\s*\[\'"Manrope"\'\s*,\s*\'sans-serif\'\]', 'body: [\'"Inter"\', \'sans-serif\']', content)
    content = re.sub(r'header:\s*\[\'"Outfit"\'\s*,\s*\'sans-serif\'\]', 'header: [\'"Google Sans"\', \'sans-serif\']', content)
    
    # 2. Fix CSS <style> block
    content = re.sub(r'h1,\s*h2,\s*h3,\s*h4,\s*h5,\s*h6\s*\{\s*font-family:\s*\'Poppins\'[^}]*\}', 'h1, h2, h3, h4, h5, h6 { font-family: \'Google Sans\', sans-serif; }', content)
    
    # Also just in case someone changed it manually to Google Sans but with different quotes
    content = re.sub(r'h1,\s*h2,\s*h3,\s*h4,\s*h5,\s*h6\s*\{\s*font-family:\s*\'Google Sans\'[^}]*\}', 'h1, h2, h3, h4, h5, h6 { font-family: \'Google Sans\', sans-serif; }', content)

    with open(filepath, 'w') as file:
        file.write(content)

print("Fonts fully mapped in Tailwind and CSS")
