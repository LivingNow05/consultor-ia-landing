import glob
import re

html_files = glob.glob('templates/*.html')

# Solid mature text (No gradients)
solid_text_css = """        .text-gradient {
            color: #171717; /* Neutral 900 */
        }
        .dark .text-gradient {
            color: #FAFAFA; /* Neutral 50 */
        }"""

# Solid typewriter cursor (No gradient, no glow/blur)
solid_cursor_css = """/* TYPEWRITER CURSOR */
    .gradient-cursor {
        display: inline-block;
        width: 3px;
        height: 1.15em;
        background-color: #171717;
        vertical-align: text-bottom;
        margin-left: 6px;
        animation: blink 1s step-end infinite;
    }
    .dark .gradient-cursor {
        background-color: #FAFAFA;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }"""

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Replace gradients
    content = re.sub(r'\.text-gradient \{.*?\}.dark \.text-gradient \{.*?\}', solid_text_css, content, flags=re.DOTALL)
    content = re.sub(r'/\* TYPEWRITER CURSOR \*/.*?@keyframes blink \{.*?\}', solid_cursor_css, content, flags=re.DOTALL)
    
    with open(filepath, 'w') as file:
        file.write(content)

# Update canvas-bg.js to be completely monochromatic (grayscale)
with open('js/canvas-bg.js', 'r') as file:
    canvas_js = file.read()

canvas_js = canvas_js.replace('const BASE_HUE = 150;', 'const BASE_HUE = 0;')
canvas_js = canvas_js.replace('const HUE_RANGE = 50;', 'const HUE_RANGE = 0;')
canvas_js = canvas_js.replace('this.s = 85;', 'this.s = 0; // Grayscale sin matices')

with open('js/canvas-bg.js', 'w') as file:
    file.write(canvas_js)

print("Matices removed, solid mature colors applied")
