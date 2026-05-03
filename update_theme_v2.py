import glob

html_files = glob.glob('templates/*.html')
for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    # Remove cursor blur
    content = content.replace('backdrop-filter: blur(2px);', '')
    
    # Replace Indigo/Purple with Neon Orange/Yellow
    content = content.replace('#6366F1', '#FF6B00') # Indigo to Neon Orange
    content = content.replace('#8B5CF6', '#FFD700') # Purple to Neon Yellow
    
    with open(f, 'w') as file:
        file.write(content)

print("Theme updated successfully")
