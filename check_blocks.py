import re
files = [
    '/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_9.md',
    '/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_10.md',
    '/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_11.md',
    '/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_12.md'
]
total = 0
for f_name in files:
    with open(f_name, 'r', encoding='utf-8') as f:
        content = f.read()
        blocks = re.findall(r'```html\n(.*?)```', content, re.DOTALL)
        print(f"{f_name[-10:]}: {len(blocks)} blocks")
        total += len(blocks)
print("Total:", total)
