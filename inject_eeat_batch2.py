import re
import csv
import glob
import os

files = [
    "/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_5.md",
    "/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_6.md",
    "/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_7.md",
    "/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_eeat_lote_8.md"
]

all_html_blocks = []
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        blocks = re.findall(r'```html\n(.*?)\n```', content, re.DOTALL)
        all_html_blocks.extend(blocks)

print(f"Total HTML blocks found: {len(all_html_blocks)}")

if len(all_html_blocks) != 40:
    print("Warning: Expected exactly 40 blocks. Aborting.")
    exit(1)

# Read CSV
csv_file = 'programatic.csv'
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

# Inject into rows 40 to 79 (which are index 40 to 79 in the rows list)
# Index of Contenido_EEAT
if 'Contenido_EEAT' not in header:
    print("Contenido_EEAT column missing!")
    exit(1)

col_idx = header.index('Contenido_EEAT')

for i, block in enumerate(all_html_blocks):
    target_row_index = 40 + i
    # Pad row if needed
    while len(rows[target_row_index]) <= col_idx:
        rows[target_row_index].append('')
    rows[target_row_index][col_idx] = block.strip()

# Write back
with open(csv_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print("programatic.csv updated with batch 2 (rows 40-79).")
