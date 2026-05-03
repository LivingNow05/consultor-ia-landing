import os
import glob

# 1. Update colors in HTML templates
html_files = glob.glob('templates/*.html')
for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    # Replace colors
    content = content.replace('#10B981', '#28D366')
    content = content.replace('#047857', '#1da851')
    content = content.replace('#34D399', '#4ade80')
    content = content.replace('rgba(16, 185, 129,', 'rgba(40, 211, 102,')
    
    with open(f, 'w') as file:
        file.write(content)

# 2. Update build.py to add H1_HTML logic
with open('build.py', 'r') as file:
    build_content = file.read()

# Add format_h1 function
format_h1_func = """
def format_h1(h1):
    if " para " in h1:
        parts = h1.split(" para ", 1)
        return f'{parts[0]} para <span class="text-gradient block mt-2">{parts[1]}</span>'
    elif ":" in h1:
        parts = h1.split(":", 1)
        return f'{parts[0]}: <span class="text-gradient block mt-2">{parts[1]}</span>'
    elif " en " in h1:
        parts = h1.split(" en ", 1)
        return f'{parts[0]} en <span class="text-gradient block mt-2">{parts[1]}</span>'
    else:
        return f'<span class="text-gradient">{h1}</span>'
"""

if "def format_h1" not in build_content:
    build_content = build_content.replace('def build():', format_h1_func + '\ndef build():')

# Replace in programatic loop
if "'{H1}': h1," in build_content:
    build_content = build_content.replace("'{H1}': h1,", "'{H1}': h1,\n                '{H1_HTML}': format_h1(h1),")

# Replace in pillar loop
if "'{H1}': row.get('H1', '')," in build_content:
    build_content = build_content.replace("'{H1}': row.get('H1', ''),", "'{H1}': row.get('H1', ''),\n                '{H1_HTML}': format_h1(row.get('H1', '')),")

with open('build.py', 'w') as file:
    file.write(build_content)

print("Update complete")
