import pandas as pd
import re
import os

# Load CSV
csv_path = 'programatic.csv'
df = pd.read_csv(csv_path)

# Ensure new column exists
if 'Contenido_EEAT' not in df.columns:
    df['Contenido_EEAT'] = ''

# Files to parse
files = [
    '/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_piloto_eeat.md',
    '/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_1.md',
    '/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_2.md',
    '/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_3.md',
    '/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_4_final.md'
]

# Extract sections
html_blocks = []
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        # Find all blocks between ```html and ```
        blocks = re.findall(r'```html(.*?)```', content, re.DOTALL)
        html_blocks.extend(blocks)

print(f"Found {len(html_blocks)} HTML blocks")

# Inject into CSV (first 40 rows)
for i in range(len(html_blocks)):
    if i < len(df):
        df.at[i, 'Contenido_EEAT'] = html_blocks[i].strip()

df.to_csv('programatic.csv', index=False)
print("CSV updated successfully.")
