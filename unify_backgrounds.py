import glob
import re

html_files = glob.glob('templates/*.html')

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # We want to replace background classes on <section> tags
    # Let's find all <section> tags and remove bg-white, bg-slate-50, dark:bg-slate-950, dark:bg-zinc-900/50, dark:bg-zinc-950/50
    
    # Define a function to clean the section class
    def clean_section(match):
        section_tag = match.group(0)
        # Remove specific bg classes
        bg_classes = [
            'bg-slate-50', 'bg-white', 'dark:bg-slate-950', 
            'dark:bg-zinc-900/50', 'dark:bg-zinc-950/50', 
            'bg-gray-50', 'dark:bg-gray-900'
        ]
        for bg in bg_classes:
            section_tag = section_tag.replace(bg + ' ', '')
            section_tag = section_tag.replace(' ' + bg, '')
            section_tag = section_tag.replace('"' + bg + '"', '""')
        return section_tag

    content = re.sub(r'<section[^>]*>', clean_section, content)
    
    with open(filepath, 'w') as file:
        file.write(content)

print("Backgrounds unified")
