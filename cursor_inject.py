import os
import glob

css = """
/* ==========================================================================
   CUSTOM PRO CURSOR
   ========================================================================== */
@media (pointer: fine) {
    body {
        cursor: none;
    }
    .custom-cursor-dot,
    .custom-cursor-aura {
        position: fixed;
        top: 0;
        left: 0;
        transform: translate(-50%, -50%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        transition: opacity 0.3s ease, width 0.3s ease, height 0.3s ease, background-color 0.3s ease;
        will-change: transform;
    }
    
    .custom-cursor-dot {
        width: 8px;
        height: 8px;
        background-color: var(--color-brand, #28D366);
        box-shadow: 0 0 10px var(--color-brand, #28D366);
    }
    
    .custom-cursor-aura {
        width: 40px;
        height: 40px;
        border: 1px solid rgba(40, 211, 102, 0.4);
        background-color: rgba(40, 211, 102, 0.05);
        box-shadow: 0 0 20px rgba(40, 211, 102, 0.2), inset 0 0 15px rgba(40, 211, 102, 0.1);
        backdrop-filter: blur(2px);
    }
    
    /* Hover state for interactive elements */
    .custom-cursor-aura.hover {
        width: 80px;
        height: 80px;
        background-color: rgba(40, 211, 102, 0.15);
        border-color: rgba(40, 211, 102, 0.8);
        box-shadow: 0 0 30px rgba(40, 211, 102, 0.4), inset 0 0 20px rgba(40, 211, 102, 0.2);
    }
    .custom-cursor-dot.hover {
        opacity: 0;
    }
}
"""

with open('index.css', 'a') as f:
    f.write(css)

js = """
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on non-touch devices
    if (window.matchMedia("(pointer: coarse)").matches) return;

    const dot = document.createElement('div');
    dot.classList.add('custom-cursor-dot');
    document.body.appendChild(dot);

    const aura = document.createElement('div');
    aura.classList.add('custom-cursor-aura');
    document.body.appendChild(aura);

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let dotX = mouseX;
    let dotY = mouseY;
    let auraX = mouseX;
    let auraY = mouseY;

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function animate() {
        // Dot follows instantly
        dotX += (mouseX - dotX) * 1;
        dotY += (mouseY - dotY) * 1;
        
        // Aura has a springy delay
        auraX += (mouseX - auraX) * 0.15;
        auraY += (mouseY - auraY) * 0.15;

        dot.style.transform = `translate3d(${dotX}px, ${dotY}px, 0) translate(-50%, -50%)`;
        aura.style.transform = `translate3d(${auraX}px, ${auraY}px, 0) translate(-50%, -50%)`;

        requestAnimationFrame(animate);
    }
    animate();

    // Add hover effects to all interactive elements
    const interactives = document.querySelectorAll('a, button, input, select, textarea, details, summary, .interactive');
    
    interactives.forEach(el => {
        el.addEventListener('mouseenter', () => {
            aura.classList.add('hover');
            dot.classList.add('hover');
        });
        el.addEventListener('mouseleave', () => {
            aura.classList.remove('hover');
            dot.classList.remove('hover');
        });
    });
});
"""

os.makedirs('js', exist_ok=True)
with open('js/custom-cursor.js', 'w') as f:
    f.write(js)

# Inject script into all templates right before </body>
html_files = glob.glob('templates/*.html')
for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    if '<script src="/js/custom-cursor.js"></script>' not in content:
        content = content.replace('</body>', '    <script src="/js/custom-cursor.js"></script>\n</body>')
        
    with open(f, 'w') as file:
        file.write(content)

print("Cursor injected successfully")
