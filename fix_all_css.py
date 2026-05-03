import glob
import re

html_files = glob.glob('templates/*.html')

correct_css = """
    /* TYPEWRITER CURSOR */
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
    }
    
    /* INTERACTIVE CANVAS BG */
    #canvas-bg {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        z-index: -1;
        pointer-events: none;
    }
    
    /* FIX OVERSCROLL (RUBBER BANDING) */
    html, body {
        overscroll-behavior: none;
    }
    </style>
"""

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Remove EVERYTHING from /* TYPEWRITER CURSOR */ up to </style> in all occurrences
    content = re.sub(r'/\* TYPEWRITER CURSOR \*/.*?</style>', '</style>', content, flags=re.DOTALL)
    
    # Now, inject the correct CSS ONLY into the first </style> which is in <head>
    # We do this by replacing the first occurrence of </style>
    content = content.replace('</style>', correct_css.strip(), 1)
    
    with open(filepath, 'w') as file:
        file.write(content)

print("CSS fully cleaned and fixed")
