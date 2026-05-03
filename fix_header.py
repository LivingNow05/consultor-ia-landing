import glob
import re

html_files = glob.glob('templates/*.html')

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # We replace the <header ...> tag and its inner <div ...container...>
    # Original: 
    # <header class="sticky top-0 z-50 glass border-b border-gray-border dark:border-zinc-800 shadow-sm">
    #     <div class="container mx-auto px-4 py-4 flex justify-between items-center">
    
    new_header = """<header class="fixed top-4 inset-x-0 z-[100] flex justify-center px-4 pointer-events-none">
        <div class="w-full max-w-7xl glass rounded-full border border-gray-200 dark:border-zinc-800/80 shadow-2xl pointer-events-auto flex justify-between items-center px-6 py-3">"""
        
    content = re.sub(
        r'<header class="sticky top-0[^>]*>\s*<div class="container mx-auto[^>]*>',
        new_header,
        content
    )
    
    # We also need to add more padding-top to the hero section because the header is now fixed (doesn't take up space in the document flow)
    content = content.replace('pt-20', 'pt-32')
    
    with open(filepath, 'w') as file:
        file.write(content)

print("Header redesigned to be floating")
