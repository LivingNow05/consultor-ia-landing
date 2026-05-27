import csv

input_file = 'programatic.csv'
output_file = 'programatic_updated.csv'

with open(input_file, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    rows = list(reader)

for row in rows:
    ind_slug = row['Industria_Slug']
    pais_slug = row['País_Slug']
    ciudad_slug = row['Ciudad_Slug']
    
    # Update URL_Final to reflect the new Industria_Slug
    row['URL_Final'] = f"/{ind_slug}/{pais_slug}/{ciudad_slug}/"

with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("URL_Final updated successfully.")
