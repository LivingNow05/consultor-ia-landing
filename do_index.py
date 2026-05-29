import sys
import os
import time

# Correct path for the indexing skill
sys.path.append('/Users/anthony/.gemini/config/skills/google-indexing-api/scripts')
try:
    from index_url_oauth import index_url
except ImportError as e:
    print(f"Error importing index_url: {e}")
    sys.exit(1)

def main():
    source_file = 'all_urls.txt'
    remaining_file = 'urls_remaining.txt'
    secrets_file = 'client_secret_225332237034-80flchf9i185nshspr3e7q0nlj5sjck7.apps.googleusercontent.com.json'
    
    # We always start from all_urls.txt because we just updated the whole site
    # So we ignore urls_remaining.txt for this new run.
    print(f"Leyendo todas las URLs de {source_file} para re-indexar los cambios visuales...")
    if not os.path.exists(source_file):
        print(f"❌ Error: No se encuentra el archivo {source_file}")
        return

    with open(source_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    # Limit to 200 per day
    total_to_process = min(len(urls), 200)
    urls_to_process = urls[:total_to_process]
    urls_leftover = urls[total_to_process:]
    
    print(f"🚀 Iniciando indexación masiva vía OAuth de {total_to_process} URLs (Cuota diaria: 200)...")

    for i, url in enumerate(urls_to_process, 1):
        print(f"\n[{i}/{total_to_process}] Procesando: {url}")
        try:
            index_url(url, secrets_file)
            time.sleep(1) 
        except Exception as e:
            print(f"⚠️ Error en {url}: {str(e)}")

    # Save remaining
    with open(remaining_file, 'w') as f:
        for u in urls_leftover:
            f.write(u + '\n')

    print(f"\n✅ Proceso completado. Se han notificado {total_to_process} URLs hoy.")
    if urls_leftover:
        print(f"ℹ️ Han quedado {len(urls_leftover)} URLs guardadas en {remaining_file}. Podrás ejecutar este proceso mañana.")

if __name__ == "__main__":
    main()
