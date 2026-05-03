import sys
import os
import time

# Añadir la ruta de la skill para poder importar el script original de OAuth
sys.path.append('/Users/anthony/.gemini/antigravity/skills/google-indexing-api/scripts')
from index_url_oauth import index_url

def main():
    urls_file = 'urls_remaining.txt'
    secrets_file = 'client_secret_225332237034-80flchf9i185nshspr3e7q0nlj5sjck7.apps.googleusercontent.com.json'
    
    if not os.path.exists(urls_file):
        print(f"❌ Error: No se encuentra el archivo {urls_file}")
        return

    with open(urls_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    total = len(urls)
    print(f"🚀 Iniciando indexación de las ÚLTIMAS {total} URLs de Consultor-IA...")

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{total}] Procesando: {url}")
        try:
            index_url(url, secrets_file)
            time.sleep(1) 
        except Exception as e:
            print(f"⚠️ Error en {url}: {str(e)}")

    print(f"\n✅ ¡MISIÓN CUMPLIDA! Se han notificado todas las URLs de Consultor-IA a Google.")

if __name__ == "__main__":
    main()
