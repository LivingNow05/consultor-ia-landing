import glob
import re

html_files = glob.glob('templates/*.html')

# New CSS for the typing cursor
typing_cursor_css = """/* TYPEWRITER CURSOR */
    .gradient-cursor {
        display: inline-block;
        width: 5px;
        height: 1.15em;
        background: linear-gradient(180deg, #28D366 0%, #0284C7 100%);
        vertical-align: text-bottom;
        margin-left: 6px;
        position: relative;
        border-radius: 4px;
        animation: blink 1s step-end infinite;
    }
    .gradient-cursor::before {
        content: '';
        position: absolute;
        inset: -2px;
        background: linear-gradient(180deg, #28D366 0%, #0284C7 100%);
        filter: blur(4px);
        z-index: -1;
        border-radius: 4px;
        opacity: 0.6;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }"""

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # 1. Remove pro-cursor logic
    content = re.sub(r'/\* PRO MINIMALIST CURSOR \*/.*?\}[\n ]*\}', '', content, flags=re.DOTALL)
    content = content.replace('<script src="/js/pro-cursor.js"></script>', '')
    
    # 2. Inject new Typing cursor CSS before </style>
    if "/* TYPEWRITER CURSOR */" not in content:
        content = content.replace('</style>', typing_cursor_css + '\n    </style>')
    
    # 3. Replace Neon Orange/Yellow with mature Green/Blue tech colors
    content = content.replace('#FF6B00', '#0284C7') # Orange -> Deep Sky Blue
    content = content.replace('#FFD700', '#0369A1') # Yellow -> Deeper Blue
    
    # Also adjust text-gradient to use these mature colors
    mature_gradient = """        .text-gradient {
            background: linear-gradient(135deg, #28D366, #0284C7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .dark .text-gradient {
            background: linear-gradient(135deg, #28D366, #38BDF8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }"""
    content = re.sub(r'\.text-gradient \{.*?\}.dark \.text-gradient \{.*?\}', mature_gradient, content, flags=re.DOTALL)
    
    with open(filepath, 'w') as file:
        file.write(content)

# Now modify build.py to inject the cursor at the end of the H1
with open('build.py', 'r') as file:
    build_content = file.read()

new_format_h1 = """def format_h1(h1):
    cursor = '<span class="gradient-cursor"></span>'
    if " para " in h1:
        parts = h1.split(" para ", 1)
        return f'{parts[0]} para <span class="text-gradient block mt-2">{parts[1]}{cursor}</span>'
    elif ":" in h1:
        parts = h1.split(":", 1)
        return f'{parts[0]}: <span class="text-gradient block mt-2">{parts[1]}{cursor}</span>'
    elif " en " in h1:
        parts = h1.split(" en ", 1)
        return f'{parts[0]} en <span class="text-gradient block mt-2">{parts[1]}{cursor}</span>'
    else:
        return f'<span class="text-gradient">{h1}{cursor}</span>'
"""

build_content = re.sub(r'def format_h1\(h1\):.*?return f\'<span class="text-gradient">\{h1\}</span>\'', new_format_h1.strip(), build_content, flags=re.DOTALL)

with open('build.py', 'w') as file:
    file.write(build_content)

print("Updates applied")
