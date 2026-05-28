import glob
import re
import os

def fix_glow_and_header(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. FIX THE GLOW FOR OLDER SAFARI
    # Replace inset: -15px with top, left, right, bottom.
    old_css = """.hover-google-glow::before {
            content: "";
            position: absolute;
            inset: -15px; /* Huge spread */"""
    
    new_css = """.hover-google-glow::before {
            content: "";
            position: absolute;
            top: -15px; left: -15px; right: -15px; bottom: -15px; /* Safari compatibility */"""
    
    if "inset: -15px;" in content:
        content = content.replace(old_css, new_css)
        content = content.replace("inset: -15px;", "top: -15px; left: -15px; right: -15px; bottom: -15px;")

    # 2. FIX HEADER CONTRAST
    # Replace text-gray-2 dark:text-slate-300 with text-zinc-600 dark:text-zinc-300
    content = content.replace("text-gray-2 dark:text-slate-300", "text-zinc-600 dark:text-zinc-300")
    content = content.replace("text-gray-2 dark:text-slate-400", "text-zinc-600 dark:text-zinc-400")

    # 3. ADD BLOBS TO HOMEPAGE (if it's build.py)
    if "build.py" in filepath:
        if "<!-- Background Animated Blobs -->" not in content and "class=\"bg-white dark:bg-zinc-950 text-zinc-900" in content:
            # We need to inject the blobs right after body starts
            blobs = """
<!-- Background Animated Blobs -->
<div class="fixed top-0 left-0 right-0 bottom-0 overflow-hidden pointer-events-none" style="z-index: -1;">
    <div class="bg-blob-1 absolute -top-[10%] -left-[10%] w-[50%] h-[50%] rounded-full bg-gradient-to-br from-[#10b981]/20 to-[#06b6d4]/20 dark:from-[#10b981]/30 dark:to-[#06b6d4]/30 blur-[100px]"></div>
    <div class="bg-blob-2 absolute top-[40%] -right-[10%] w-[60%] h-[60%] rounded-full bg-gradient-to-br from-[#8b5cf6]/20 to-[#ec4899]/20 dark:from-[#8b5cf6]/30 dark:to-[#ec4899]/30 blur-[120px]"></div>
</div>
"""
            content = content.replace('class="bg-white dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 transition-colors duration-300">\n', 
                                      'class="bg-white dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 transition-colors duration-300">\n' + blobs)
            
            # Also inject the CSS for the blobs into build_home_page
            blob_css = """
        /* Background Animated Blobs */
        @keyframes blob-move-1 {
            0% { transform: translate(0, 0) scale(1) rotate(0deg); }
            33% { transform: translate(15vw, -10vh) scale(1.2) rotate(15deg); }
            66% { transform: translate(-10vw, 15vh) scale(0.8) rotate(-15deg); }
            100% { transform: translate(0, 0) scale(1) rotate(0deg); }
        }
        @keyframes blob-move-2 {
            0% { transform: translate(0, 0) scale(1) rotate(0deg); }
            33% { transform: translate(-15vw, 15vh) scale(1.2) rotate(-15deg); }
            66% { transform: translate(15vw, -10vh) scale(0.8) rotate(15deg); }
            100% { transform: translate(0, 0) scale(1) rotate(0deg); }
        }
        .bg-blob-1 { animation: blob-move-1 12s infinite ease-in-out; }
        .bg-blob-2 { animation: blob-move-2 15s infinite ease-in-out; }
"""
            if "blob-move-1" not in content and "build_home_page" in content:
                content = content.replace('</style>', blob_css + '    </style>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

files = glob.glob('templates/*.html') + glob.glob('dist/blog/*/index.html') + ['build.py', 'build_blog.py']
for f in files:
    try:
        fix_glow_and_header(f)
        print(f"Fixed {f}")
    except Exception as e:
        print(f"Error on {f}: {e}")

print("Safari and Homepage fixes applied.")
