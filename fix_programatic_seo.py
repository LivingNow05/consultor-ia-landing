import csv
import os

CSV_FILE = "programatic.csv"

def fix_seo_metadata():
    if not os.path.exists(CSV_FILE):
        print("CSV file not found")
        return

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    updated_count = 0
    for row in rows:
        ciudad = row.get("Ciudad", "").strip()
        industria = row.get("Industria", "").strip()
        moneda = row.get("Moneda", "COP").strip()
        
        meta = row.get("Meta_Description", "")
        title = row.get("Title_SEO", "")
        
        # 1. Fix truncated or low-quality Meta_Description
        if "recupera clien" in meta or len(meta) < 120 or "WhatsApp 24/7." in meta:
            new_meta = f"Agente de IA para {industria} en {ciudad}. Automatiza reservas 24/7, catálogo de servicios, atención sin comisiones y recuperación de clientes. ¡Solicita tu Demo!"
            row["Meta_Description"] = new_meta
            updated_count += 1
            
        # 2. Enhance Title_SEO with CTR Hooks
        if title and not title.startswith("🤖") and "[" not in title:
            new_title = f"🤖 Chatbot WhatsApp para {industria} en {ciudad}: Agente IA 24/7 [{moneda}]"
            row["Title_SEO"] = new_title

    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully updated {updated_count} rows in {CSV_FILE} with optimized SEO metadata.")

if __name__ == "__main__":
    fix_seo_metadata()
