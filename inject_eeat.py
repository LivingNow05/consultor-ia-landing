import re
import pandas as pd
import glob

files = [
    "/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_piloto_eeat.md",
    "/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_1.md",
    "/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_2.md",
    "/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_3.md",
    "/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_4_final.md"
]

all_html_blocks = []

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        blocks = re.findall(r'```html\n(.*?)\n```', content, re.DOTALL)
        all_html_blocks.extend(blocks)

print(f"Total HTML blocks found: {len(all_html_blocks)}")

df = pd.read_csv('programatic.csv')

if 'Contenido_EEAT' not in df.columns:
    df['Contenido_EEAT'] = ""

for i, block in enumerate(all_html_blocks):
    if i < len(df):
        df.loc[i, 'Contenido_EEAT'] = block

df.to_csv('programatic.csv', index=False)
print("programatic.csv updated with Contenido_EEAT")
