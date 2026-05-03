import glob
import re

html_files = glob.glob('templates/*.html')

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Header logo replacement
    # We want to replace the exact block of the header logo
    old_header_logo = r'<a href="/" class="text-2xl font-header font-normal text-brand dark:text-brand-light flex items-center gap-2">\s*<span class="font-header font-normal tracking-tighter text-3xl">Consultor IA</span>\s*</a>'
    new_header_logo = """<a href="/" class="text-2xl font-header flex items-center gap-2">
                <span class="font-header font-extrabold tracking-tighter text-3xl text-zinc-900 dark:text-white">Consultor<span class="text-brand">IA</span></span>
            </a>"""
            
    content = re.sub(old_header_logo, new_header_logo, content)
    
    # Footer logo replacement
    old_footer_logo = r'<a href="/" class="text-2xl font-header font-normal text-white flex items-center justify-center md:justify-start gap-2 mb-2">\s*<span class="font-header font-normal tracking-tighter text-3xl text-white">Consultor IA</span>\s*</a>'
    new_footer_logo = """<a href="/" class="text-2xl font-header flex items-center justify-center md:justify-start gap-2 mb-2">
                    <span class="font-header font-extrabold tracking-tighter text-3xl text-white">Consultor<span class="text-brand">IA</span></span>
                </a>"""
                
    content = re.sub(old_footer_logo, new_footer_logo, content)
    
    with open(filepath, 'w') as file:
        file.write(content)

print("Logo redesigned")
