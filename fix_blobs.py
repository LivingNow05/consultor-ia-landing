import glob
import re
import os

BLOBS_CSS = """
        /* Smooth Global Background Blobs */
        @keyframes global-blob-1 {
            0% { transform: translate(0, 0) scale(1) rotate(0deg); }
            33% { transform: translate(20vw, -15vh) scale(1.2) rotate(10deg); }
            66% { transform: translate(-15vw, 20vh) scale(0.8) rotate(-10deg); }
            100% { transform: translate(0, 0) scale(1) rotate(0deg); }
        }
        @keyframes global-blob-2 {
            0% { transform: translate(0, 0) scale(1) rotate(0deg); }
            33% { transform: translate(-20vw, 20vh) scale(1.3) rotate(-15deg); }
            66% { transform: translate(20vw, -15vh) scale(0.7) rotate(15deg); }
            100% { transform: translate(0, 0) scale(1) rotate(0deg); }
        }
        @keyframes global-blob-3 {
            0% { transform: translate(0, 0) scale(1) rotate(0deg); }
            50% { transform: translate(25vw, 25vh) scale(1.4) rotate(20deg); }
            100% { transform: translate(0, 0) scale(1) rotate(0deg); }
        }
        .global-blob-1 { animation: global-blob-1 12s infinite alternate ease-in-out; }
        .global-blob-2 { animation: global-blob-2 15s infinite alternate ease-in-out; }
        .global-blob-3 { animation: global-blob-3 18s infinite alternate ease-in-out; }
"""

BLOBS_HTML = """
<!-- Smooth Global Background Blobs -->
<div class="fixed top-0 left-0 right-0 bottom-0 overflow-hidden pointer-events-none" style="z-index: -1;">
    <div class="global-blob-1 absolute -top-[20%] -left-[10%] w-[60vw] h-[60vw] md:w-[40vw] md:h-[40vw] rounded-full bg-gradient-to-br from-[#10b981]/10 to-[#06b6d4]/10 dark:from-[#10b981]/15 dark:to-[#06b6d4]/15 blur-[100px] md:blur-[150px]"></div>
    <div class="global-blob-2 absolute top-[20%] -right-[10%] w-[70vw] h-[70vw] md:w-[50vw] md:h-[50vw] rounded-full bg-gradient-to-br from-[#8b5cf6]/10 to-[#ec4899]/10 dark:from-[#8b5cf6]/15 dark:to-[#ec4899]/15 blur-[100px] md:blur-[150px]"></div>
    <div class="global-blob-3 absolute -bottom-[20%] left-[20%] w-[60vw] h-[60vw] md:w-[45vw] md:h-[45vw] rounded-full bg-gradient-to-br from-[#3b82f6]/10 to-[#8b5cf6]/10 dark:from-[#3b82f6]/15 dark:to-[#8b5cf6]/15 blur-[100px] md:blur-[150px]"></div>
</div>
"""

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Remove hover-google-glow class
    content = content.replace(' hover-google-glow', '')
    content = content.replace('hover-google-glow ', '')

    # 2. Remove all related CSS blocks
    content = re.sub(r'\s*/\*\s*Glow Hover Effect.*?(?=(</style>|/\*\s*Background Animated Blobs))', '\n', content, flags=re.DOTALL)
    content = re.sub(r'\s*/\*\s*Background Animated Blobs.*?\.bg-blob-2\s*\{\s*animation:.*?\}', '\n', content, flags=re.DOTALL)
    
    # Clean up old blob HTML
    content = re.sub(r'\s*<!-- Background Animated Blobs -->.*?</div>\s*</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'\s*<!-- Smooth Global Background Blobs -->.*?</div>\s*</div>', '', content, flags=re.DOTALL)
    
    # Clean up any residual CSS block for global blobs so we don't duplicate
    content = re.sub(r'\s*/\*\s*Smooth Global Background Blobs.*?(?=</style>)', '\n', content, flags=re.DOTALL)

    # 3. Inject new CSS
    css_to_inject = BLOBS_CSS
    if filepath.endswith('.py'):
        # In Python files, the HTML is often an f-string, so CSS braces must be double-escaped
        css_to_inject = css_to_inject.replace('{', '{{').replace('}', '}}')

    if "</style>" in content:
        content = content.replace("</style>", css_to_inject + "    </style>")

    # 4. Inject new HTML right after body
    body_pattern = re.compile(r'(<body[^>]*>)')
    content = body_pattern.sub(r'\1\n' + BLOBS_HTML, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

def main():
    files_to_check = glob.glob('templates/*.html') + ['build.py', 'build_blog.py']
    for f in files_to_check:
        try:
            fix_file(f)
        except Exception as e:
            print(f"Error processing {f}: {e}")

if __name__ == '__main__':
    main()
