import sys
import os
import time

# Añadir la ruta de la skill para poder importar el script original
sys.path.append('/Users/anthony/.gemini/antigravity/skills/google-indexing-api/scripts')
from index_url import index_url

def main():
    urls_file = 'urls_to_index.txt'
    key_path = 'service-account.json'
    
    if not os.path.exists(urls_file):
        print(f"❌ Error: No se encuentra el archivo {urls_file}")
        return

    with open(urls_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    total = len(urls)
    print(f"🚀 Iniciando indexación masiva de {total} URLs...")

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{total}] Procesando: {url}")
        try:
            index_url(url, key_path)
            # Pequeña pausa para no saturar la cuota de la API
            time.sleep(0.5) 
        except Exception as e:
            print(f"⚠️ Error en {url}: {str(e)}")

    print("\n✅ Proceso de indexación masiva completado.")

if __name__ == "__main__":
    main()
