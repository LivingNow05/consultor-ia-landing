import os
import glob

css = """
/* CUSTOM PRO CURSOR */
@media (pointer: fine) {
    body { cursor: none; }
    .custom-cursor-dot, .custom-cursor-aura {
        position: fixed;
        top: 0; left: 0;
        transform: translate(-50%, -50%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        transition: opacity 0.3s ease, width 0.3s ease, height 0.3s ease, background-color 0.3s ease, border-color 0.3s ease;
        will-change: transform;
    }
    .custom-cursor-dot {
        width: 8px; height: 8px;
        background-color: var(--color-brand, #28D366);
        box-shadow: 0 0 10px var(--color-brand, #28D366);
    }
    .custom-cursor-aura {
        width: 40px; height: 40px;
        border: 1px solid rgba(40, 211, 102, 0.4);
        background-color: rgba(40, 211, 102, 0.05);
        box-shadow: 0 0 20px rgba(40, 211, 102, 0.2), inset 0 0 15px rgba(40, 211, 102, 0.1);
        backdrop-filter: blur(2px);
    }
    .custom-cursor-aura.hover {
        width: 80px; height: 80px;
        background-color: rgba(40, 211, 102, 0.15);
        border-color: rgba(40, 211, 102, 0.8);
        box-shadow: 0 0 30px rgba(40, 211, 102, 0.4), inset 0 0 20px rgba(40, 211, 102, 0.2);
    }
    .custom-cursor-dot.hover { opacity: 0; }
}
"""

html_files = glob.glob('templates/*.html')
for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    if "/* CUSTOM PRO CURSOR */" not in content:
        content = content.replace('</style>', css + '\n    </style>')
        
    with open(f, 'w') as file:
        file.write(content)

print("CSS injected successfully")
