import csv
import re

def fix_eeat_csv():
    csv_file = 'programatic.csv'
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    blocks = [r.get('Contenido_EEAT', '') for r in rows if r.get('Contenido_EEAT')]
    print(f"Total rows in CSV: {len(rows)}")
    print(f"Total EEAT blocks available: {len(blocks)}")

    def score_pair(row, block):
        city = row.get('Ciudad', '').strip().lower()
        ind = row.get('Industria', '').strip().lower()
        slug = row.get('Slug_Industria', '').strip().lower()
        b_lower = block.lower()
        
        score = 0
        city_aliases = [city]
        if 'ciudad de méxico' in city: city_aliases.extend(['cdmx', 'mexico'])
        if 'buenos aires' in city: city_aliases.extend(['porteño', 'porteña'])
        if 'medellín' in city: city_aliases.extend(['paisa'])
        if 'cali' in city: city_aliases.extend(['caleño', 'caleña'])
        if 'barranquilla' in city: city_aliases.extend(['barranquillero', 'curramba'])
        
        if any(ca in b_lower for ca in city_aliases):
            score += 100
            
        if slug in b_lower:
            score += 50
            
        for w in ind.split():
            if len(w) > 3 and w in b_lower:
                score += 20
                
        return score

    matrix = []
    for r in rows:
        matrix.append([score_pair(r, b) for b in blocks])

    pairs = []
    for i in range(len(rows)):
        for j in range(len(blocks)):
            if matrix[i][j] > 0:
                pairs.append((matrix[i][j], i, j))

    pairs.sort(key=lambda x: x[0], reverse=True)

    assigned_rows = {}
    assigned_blocks = {}

    for score, r_idx, b_idx in pairs:
        if r_idx not in assigned_rows and b_idx not in assigned_blocks:
            assigned_rows[r_idx] = b_idx
            assigned_blocks[b_idx] = r_idx

    remaining_rows = [i for i in range(len(rows)) if i not in assigned_rows]
    remaining_blocks = [j for j in range(len(blocks)) if j not in assigned_blocks]

    for r_i, b_j in zip(remaining_rows, remaining_blocks):
        assigned_rows[r_i] = b_j

    print(f"Successfully realigned {len(assigned_rows)} rows 1-to-1.")

    for i in range(len(rows)):
        b_idx = assigned_rows[i]
        rows[i]['Contenido_EEAT'] = blocks[b_idx]

    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("programatic.csv saved successfully with realigned Contenido_EEAT.")

if __name__ == '__main__':
    fix_eeat_csv()
