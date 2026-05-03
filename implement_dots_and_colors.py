import re

# 1. Update build.py to use solid text-brand instead of text-gradient
with open('build.py', 'r') as file:
    build_content = file.read()

new_format_h1 = """def format_h1(h1):
    cursor = '<span class="typewriter-cursor"></span>'
    if " para " in h1:
        parts = h1.split(" para ", 1)
        return f'{parts[0]} para <span class="text-brand block mt-2">{parts[1]}{cursor}</span>'
    elif ":" in h1:
        parts = h1.split(":", 1)
        return f'{parts[0]}: <span class="text-brand block mt-2">{parts[1]}{cursor}</span>'
    elif " en " in h1:
        parts = h1.split(" en ", 1)
        return f'{parts[0]} en <span class="text-brand block mt-2">{parts[1]}{cursor}</span>'
    else:
        return f'<span class="text-brand">{h1}{cursor}</span>'
"""
build_content = re.sub(r'def format_h1\(h1\):.*?return f\'<span class="text-gradient">\{h1\}\{cursor\}</span>\'\n', new_format_h1, build_content, flags=re.DOTALL)

with open('build.py', 'w') as file:
    file.write(build_content)

# 2. Update all templates to change gradient-cursor to typewriter-cursor (solid)
import glob
html_files = glob.glob('templates/*.html')

cursor_css = """/* TYPEWRITER CURSOR */
    .typewriter-cursor {
        display: inline-block;
        width: 3px;
        height: 1.15em;
        background-color: var(--color-brand);
        vertical-align: text-bottom;
        margin-left: 6px;
        animation: blink 1s step-end infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }"""

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # We remove the old gradient cursor and broken text-gradient
    content = re.sub(r'\.text-gradient \{.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\.gradient-cursor \{.*?@keyframes blink \{.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* TYPEWRITER CURSOR \*/.*?@keyframes blink \{.*?\}', cursor_css, content, flags=re.DOTALL)
    
    # If the old css was removed but not replaced, ensure it's there
    if "/* TYPEWRITER CURSOR */" not in content:
        content = content.replace('</style>', cursor_css + '\n    </style>')
        
    with open(filepath, 'w') as file:
        file.write(content)

# 3. Update canvas-bg.js to use Dots instead of Lines
with open('js/canvas-bg.js', 'r') as file:
    canvas_js = file.read()

# Replace draw function
old_draw = """        draw() {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.angle);

            ctx.beginPath();
            ctx.lineCap = 'round';
            ctx.lineWidth = 2;

            const len = config.baseLength * this.scale;

            ctx.moveTo(-len / 2, 0);
            ctx.lineTo(len / 2, 0);

            ctx.strokeStyle = `hsla(${this.h}, ${this.s}%, ${this.l}%, ${this.a})`;
            ctx.stroke();

            ctx.restore();
        }"""

new_draw = """        draw() {
            ctx.save();
            ctx.translate(this.x, this.y);

            ctx.beginPath();
            
            // Draw a dot that scales up when mouse is near
            const radius = 2.5 * this.scale;
            ctx.arc(0, 0, radius, 0, Math.PI * 2);
            
            ctx.fillStyle = `hsla(${this.h}, ${this.s}%, ${this.l}%, ${this.a})`;
            ctx.fill();

            ctx.restore();
        }"""

canvas_js = canvas_js.replace(old_draw, new_draw)

with open('js/canvas-bg.js', 'w') as file:
    file.write(canvas_js)

print("Updates applied")
