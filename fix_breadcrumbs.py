import glob
import re

html_files = glob.glob('templates/*.html')

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Target the Breadcrumbs div:
    # <div class="bg-slate-50 dark:bg-zinc-900 border-b border-gray-border dark:border-zinc-800">
    # We'll change it to be transparent and have top padding to clear the header
    old_div = r'<div class="bg-slate-50 dark:bg-zinc-900 border-b border-gray-border dark:border-zinc-800">'
    new_div = '<div class="pt-24 pb-2 border-b border-gray-200/50 dark:border-zinc-800/50 relative z-10">'
    
    content = re.sub(old_div, new_div, content)
    
    with open(filepath, 'w') as file:
        file.write(content)

print("Breadcrumbs fixed")
