import re

with open('templates/template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Extract header
header_match = re.search(r'(<header.*?</header>)', template, re.DOTALL)
header_html = header_match.group(1) if header_match else "{MEGA_MENU}"

# Extract mobile menu
mobile_match = re.search(r'(<!-- Mobile Menu Overlay -->.*?</div>\s*</div>)', template, re.DOTALL)
mobile_html = mobile_match.group(1) if mobile_match else ""

for filename in ['templates/hub-industria.html', 'templates/hub-pais.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace literal {MEGA_MENU} with the full header
    content = content.replace('{MEGA_MENU}', header_html)
    
    # Add mobile menu right before script
    if mobile_html not in content:
        content = content.replace('<!-- Dark Mode Toggle Script -->', mobile_html + '\n\n    <!-- Dark Mode Toggle Script -->')
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed hub templates with proper header.")
