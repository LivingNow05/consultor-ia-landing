import os
import glob

html_files = glob.glob('templates/*.html')

old_button_content = """class="group relative inline-flex w-full items-center justify-center border border-zinc-900 dark:border-white px-8 py-3.5 overflow-hidden transition-all duration-500">
                            <span class="absolute inset-0 w-full h-full bg-zinc-900 dark:bg-white origin-bottom scale-y-0 transition-transform duration-500 ease-[cubic-bezier(0.7,0,0.3,1)] group-hover:scale-y-100"></span>
                            <span class="relative z-10 flex items-center gap-3 font-body text-[11px] font-bold uppercase tracking-[0.2em] text-zinc-900 dark:text-white group-hover:text-white dark:group-hover:text-zinc-900 transition-colors duration-500 delay-75">"""

new_button_content = """class="group relative inline-flex w-full items-center justify-center border border-white px-8 py-3.5 rounded-xl overflow-hidden transition-all duration-500">
                            <span class="absolute inset-0 w-full h-full bg-white origin-bottom scale-y-0 transition-transform duration-500 ease-[cubic-bezier(0.7,0,0.3,1)] group-hover:scale-y-100"></span>
                            <span class="relative z-10 flex items-center gap-3 font-body text-[11px] font-bold uppercase tracking-[0.2em] text-white group-hover:text-zinc-900 transition-colors duration-500 delay-75">"""

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_button_content in content:
        content = content.replace(old_button_content, new_button_content)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {file}")
    else:
        print(f"Content not found in {file}")

