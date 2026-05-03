import glob
import re

html_files = glob.glob('templates/*.html')

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # We want to remove font-bold, font-semibold, and font-medium from <p>, <span>, <a>, <li>
    # However, we don't want to remove it from the logo span or button tags.
    # Instead of complex regex, let's just do it broadly for font-medium and font-semibold, 
    # and selectively for font-bold on p, li, span.
    
    def remove_weight(match):
        tag = match.group(0)
        
        # Don't modify the logo or CTA buttons
        if 'Consultor IA' in tag or 'btn' in tag or 'Hablar con un Experto' in tag or 'Ver Arquitectura' in tag:
            return tag
            
        tag = tag.replace('font-bold', 'font-normal')
        tag = tag.replace('font-semibold', 'font-normal')
        tag = tag.replace('font-medium', 'font-normal')
        # Clean up
        tag = tag.replace('font-normal font-normal', 'font-normal')
        return tag

    # Apply to all standard text tags
    content = re.sub(r'<(p|span|a|li|div)[^>]*>', remove_weight, content)
    
    with open(filepath, 'w') as file:
        file.write(content)

print("Font weights reduced")
