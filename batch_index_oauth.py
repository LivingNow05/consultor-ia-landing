import sys
import os
import time

# Añadir la ruta de la skill para poder importar el script original de OAuth
sys.path.append('/Users/anthony/.gemini/antigravity/skills/google-indexing-api/scripts')
from index_url_oauth import index_url

def main():
    urls_file = 'urls_to_index.txt'
    # Usando el archivo de secretos que mencionaste
    secrets_file = 'client_secret_225332237034-80flchf9i185nshspr3e7q0nlj5sjck7.apps.googleusercontent.com.json'
    
    if not os.path.exists(urls_file):
        print(f"❌ Error: No se encuentra el archivo {urls_file}")
        return

    with open(urls_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    # Limitamos a 200 por hoy debido a la cuota diaria de la API
    total_to_process = min(len(urls), 200)
    urls_to_process = urls[:total_to_process]
    
    print(f"🚀 Iniciando indexación masiva vía OAuth de {total_to_process} URLs (Cuota diaria: 200)...")

    for i, url in enumerate(urls_to_process, 1):
        print(f"\n[{i}/{total_to_process}] Procesando: {url}")
        try:
            # El primer llamado abrirá el navegador para autenticarte
            index_url(url, secrets_file)
            # Pausa para respetar la API
            time.sleep(1) 
        except Exception as e:
            print(f"⚠️ Error en {url}: {str(e)}")

    print(f"\n✅ Proceso completado. Se han notificado {total_to_process} URLs hoy.")
    if len(urls) > 200:
        print(f"ℹ️ Mañana podremos procesar las {len(urls) - 200} restantes.")

if __name__ == "__main__":
    main()
