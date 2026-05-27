import csv

input_file = 'programatic.csv'
output_file = 'programatic_updated.csv'

with open(input_file, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    rows = list(reader)

for row in rows:
    slug = row['Industria_Slug']
    if not slug.startswith('ia-para-'):
        row['Industria_Slug'] = f"ia-para-{slug}"

with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Slugs updated successfully.")
