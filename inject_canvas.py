import glob
import re

html_files = glob.glob('templates/*.html')

canvas_css = """/* INTERACTIVE CANVAS BG */
    #canvas-bg {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        z-index: -1;
        pointer-events: none;
    }"""

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Add canvas CSS if not present
    if "/* INTERACTIVE CANVAS BG */" not in content:
        content = content.replace('</style>', canvas_css + '\n    </style>')
    
    # Add script if not present
    if '<script src="/js/canvas-bg.js"></script>' not in content:
        content = content.replace('</body>', '    <script src="/js/canvas-bg.js"></script>\n</body>')
    
    with open(filepath, 'w') as file:
        file.write(content)

print("Canvas background injected")
