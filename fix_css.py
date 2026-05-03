import glob
import re

html_files = glob.glob('templates/*.html')

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Remove the broken syntax
    content = content.replace("        50% { opacity: 0; }\n    }\n        50% { opacity: 0; }\n    }", "")
    # Wait, it might be slightly different whitespace. Let's just use regex to clean up everything between @keyframes blink and /* INTERACTIVE CANVAS BG */
    content = re.sub(r'@keyframes blink \{[\s\S]*?\}[\s\S]*?(?=/\* INTERACTIVE CANVAS BG \*/)', 
                     '@keyframes blink {\n        0%, 100% { opacity: 1; }\n        50% { opacity: 0; }\n    }\n    ', content)
                     
    with open(filepath, 'w') as file:
        file.write(content)

print("CSS fixed")
