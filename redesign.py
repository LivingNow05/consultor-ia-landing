import os
import glob
import re

html_files = glob.glob('templates/*.html')

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # 1. Fonts
    content = content.replace(
        'family=Poppins:wght@600;700&family=Inter:wght@400;500;600&display=swap',
        'family=Outfit:wght@500;600;700;800&family=Manrope:wght@400;500;600&display=swap'
    )
    content = content.replace("body: ['\"Inter\"', 'sans-serif']", "body: ['\"Manrope\"', 'sans-serif']")
    content = content.replace("header: ['\"Poppins\"', 'sans-serif']", "header: ['\"Outfit\"', 'sans-serif']")
    
    # 2. Icons
    content = content.replace('<i class="fas fa-brain"></i> Consultor IA', '<span class="font-header font-bold tracking-tighter text-xl">Consultor IA</span>')
    content = content.replace('<i class="fas fa-brain text-brand-light"></i> Consultor IA', '<span class="font-header font-bold tracking-tighter text-xl text-white">Consultor IA</span>')
    
    # 3. Blobs
    content = re.sub(r'<div class="blob blob-\d+"></div>', '', content)
    content = re.sub(r'\.blob \{.*?\n.*?\n.*?\n', '', content)
    
    # 4. Minimalist background and border classes
    content = content.replace('bg-[#05050A]', 'bg-[#09090b]') # Zinc 950
    content = content.replace('border-gray-800', 'border-zinc-800')
    content = content.replace('dark:bg-slate-900', 'dark:bg-zinc-900')
    content = content.replace('dark:bg-slate-800', 'dark:bg-zinc-800')
    content = content.replace('dark:border-slate-800', 'dark:border-zinc-800')
    content = content.replace('bg-gray-card', 'bg-slate-50')
    
    # 5. Buttons (Remove border-beam, make minimalist)
    # The button uses: border-beam px-8 py-4 bg-white dark:bg-slate-900 ...
    content = re.sub(r'border-beam (px-\d+ py-\d+) bg-white dark:bg-slate-900[^>]*>', 
                     r'\1 bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 font-bold rounded-full shadow-lg hover:scale-105 transition-transform duration-300>', content)
    
    # Also for "Agendar Consultoría" on nav
    content = content.replace('bg-brand hover:bg-brand-dark text-white', 'bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200')
    
    # 6. Text Gradients (Make them pure accent color or solid)
    # Instead of linear-gradient, let's just make it the brand color
    css_gradient = """        .text-gradient {
            color: var(--color-brand);
        }
        .dark .text-gradient {
            color: var(--color-brand);
        }"""
    content = re.sub(r'\.text-gradient \{.*?\}.dark \.text-gradient \{.*?\}', css_gradient, content, flags=re.DOTALL)
    
    # 7. Cursor CSS (Remove old, add new blend-mode cursor)
    new_cursor_css = """/* PRO MINIMALIST CURSOR */
@media (pointer: fine) {
    body { cursor: none; }
    .pro-cursor {
        position: fixed;
        top: 0; left: 0;
        width: 16px; height: 16px;
        background-color: white;
        border-radius: 50%;
        pointer-events: none;
        z-index: 10000;
        mix-blend-mode: difference;
        transform: translate(-50%, -50%);
        transition: width 0.3s cubic-bezier(0.16, 1, 0.3, 1), height 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        will-change: transform, width, height;
    }
    .pro-cursor.hover {
        width: 60px; height: 60px;
    }
}"""
    # Replace old cursor css
    content = re.sub(r'/\* CUSTOM PRO CURSOR \*/.*?\}[\n ]*\}', new_cursor_css, content, flags=re.DOTALL)
    
    # Replace the JS include if it's the old one
    content = content.replace('/js/custom-cursor.js', '/js/pro-cursor.js')
    
    with open(filepath, 'w') as file:
        file.write(content)

print("HTML Templates updated for redesign")
