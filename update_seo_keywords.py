import csv
import os

CSV_FILE = 'programatic.csv'
BACKUP_FILE = 'programatic_backup.csv'

def main():
    # Create a backup
    import shutil
    shutil.copyfile(CSV_FILE, BACKUP_FILE)

    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    for row in rows:
        # Update H1
        # Original: Inteligencia Artificial y Agentes IA para Restaurantes en Bogotá
        row['H1'] = f"Chatbot de WhatsApp para {row['Industria']} en {row['Ciudad']}"

        # Update Title_SEO
        # Original: Inteligencia Artificial y Agentes IA para Restaurantes en Bogotá 2026 | Consultor IA
        row['Title_SEO'] = f"Chatbot de WhatsApp para {row['Industria']} en {row['Ciudad']} 2026 | Consultor IA"

        # Update Meta Description
        # e.g., Implementamos agentes IA para restaurantes en Bogotá...
        meta = row['Meta_Description']
        meta = meta.replace('agentes IA', 'chatbots de WhatsApp')
        meta = meta.replace('Agentes IA', 'Chatbots de WhatsApp')
        meta = meta.replace('Agente IA', 'Chatbot de WhatsApp')
        meta = meta.replace('agente IA', 'chatbot de WhatsApp')
        row['Meta_Description'] = meta

        # Swap Keywords if Keyword_Secundaria has 'chatbot whatsapp'
        kw_p = row['Keyword_Principal']
        kw_s = row['Keyword_Secundaria']
        
        if 'chatbot whatsapp' in kw_s.lower() and 'agente ia' in kw_p.lower():
            row['Keyword_Principal'] = kw_s
            row['Keyword_Secundaria'] = kw_p
        else:
            # Fallback if they are not exactly as expected
            row['Keyword_Principal'] = f"chatbot whatsapp {row['Industria_Singular']} {row['Ciudad']}".lower()

    # Write back
    with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully updated {len(rows)} rows in {CSV_FILE}.")

if __name__ == '__main__':
    main()
