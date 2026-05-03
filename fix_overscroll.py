import glob
import re

html_files = glob.glob('templates/*.html')

css_fix = """
    /* FIX OVERSCROLL (RUBBER BANDING) */
    html, body {
        overscroll-behavior: none;
        background-color: #09090b; /* Fallback for dark mode rubber band */
    }
"""

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    if "/* FIX OVERSCROLL" not in content:
        content = content.replace('</style>', css_fix + '\n    </style>')
    
    with open(filepath, 'w') as file:
        file.write(content)

print("Overscroll fixed")
