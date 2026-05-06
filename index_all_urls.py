#!/usr/bin/env python3
"""
index_all_urls.py
Envía todas las URLs de consultor-ia.com.co a la Google Indexing API.

REQUISITOS:
  pip install google-auth requests

CREDENCIALES:
  - Descarga el archivo service-account.json desde Google Cloud Console.
  - Agrégalo en este mismo directorio como: service-account.json
  - El correo de la cuenta de servicio DEBE estar como "Propietario" en Google Search Console.

USO:
  python3 index_all_urls.py                  # Indexa todas las URLs
  python3 index_all_urls.py --dry-run        # Solo muestra cuántas URLs procesaría
  python3 index_all_urls.py --limit 50       # Solo indexa las primeras 50 URLs
"""

import argparse
import json
import os
import time
import requests
import sys

try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request as GoogleRequest
except ImportError:
    print("❌ Dependencia faltante. Ejecuta: pip install google-auth requests")
    sys.exit(1)

# ────────────────────────────────────────────────────────────
CREDENTIALS_FILE = "service-account.json"
INDEXING_API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]
URL_LIST_FILE = "all_urls.txt"
DELAY_BETWEEN_REQUESTS = 0.5   # segundos entre petición y petición
MAX_QUOTA_PER_RUN = 200        # límite diario de la API gratuita es 200
# ────────────────────────────────────────────────────────────


def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ No se encontró el archivo: {CREDENTIALS_FILE}")
        print("   → Descárgalo desde Google Cloud Console (IAM > Cuentas de Servicio > Claves)")
        print("   → Guárdalo en este directorio con el nombre: service-account.json")
        sys.exit(1)
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    creds.refresh(GoogleRequest())
    return creds


def get_access_token(creds):
    creds.refresh(GoogleRequest())
    return creds.token


def notify_url(url, token, notification_type="URL_UPDATED"):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = {"url": url, "type": notification_type}
    response = requests.post(INDEXING_API_URL, headers=headers, json=body)
    return response.status_code, response.json()


def load_urls(limit=None):
    if not os.path.exists(URL_LIST_FILE):
        print(f"❌ No se encontró {URL_LIST_FILE}. Ejecuta primero: python3 generate_sitemap.py")
        sys.exit(1)
    with open(URL_LIST_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    if limit:
        urls = urls[:limit]
    return urls


def run(dry_run=False, limit=None):
    urls = load_urls(limit=limit)
    total = len(urls)
    print(f"\n📋 URLs a indexar: {total}")

    if total > MAX_QUOTA_PER_RUN:
        print(f"⚠️  La cuota diaria gratuita es {MAX_QUOTA_PER_RUN} URLs.")
        print(f"   Se procesarán solo las primeras {MAX_QUOTA_PER_RUN}. Ejecuta de nuevo mañana para el resto.")
        urls = urls[:MAX_QUOTA_PER_RUN]
        total = MAX_QUOTA_PER_RUN

    if dry_run:
        print(f"\n✅ [DRY RUN] Se enviarían {total} URLs. No se realizó ninguna petición.")
        for u in urls[:5]:
            print(f"   → {u}")
        if len(urls) > 5:
            print(f"   ... y {len(urls) - 5} más.")
        return

    creds = load_credentials()
    print(f"🔑 Autenticado como: {creds.service_account_email}\n")

    success = 0
    failed = 0
    log_entries = []

    for i, url in enumerate(urls, 1):
        # Refresh token every 50 requests to avoid expiry
        if i % 50 == 1:
            token = get_access_token(creds)

        status, resp = notify_url(url, token)
        ok = status == 200

        icon = "✅" if ok else "❌"
        msg = resp.get("urlNotificationMetadata", {}).get("latestUpdate", {}).get("type", resp.get("error", {}).get("message", "?"))
        print(f"[{i:03d}/{total}] {icon} {url}")
        if not ok:
            print(f"         Error {status}: {msg}")
            failed += 1
        else:
            success += 1

        log_entries.append({"url": url, "status": status, "response": resp})
        time.sleep(DELAY_BETWEEN_REQUESTS)

    # Save log
    log_file = "indexing_log.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_entries, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"🏁 RESULTADO FINAL")
    print(f"   ✅ Exitosas: {success}")
    print(f"   ❌ Fallidas: {failed}")
    print(f"   📄 Log completo: {log_file}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indexa consultor-ia.com.co vía Google Indexing API")
    parser.add_argument("--dry-run", action="store_true", help="Solo muestra cuántas URLs se procesarían, sin hacer peticiones.")
    parser.add_argument("--limit", type=int, default=None, help="Limita el número de URLs a indexar (ej: --limit 50).")
    args = parser.parse_args()
    run(dry_run=args.dry_run, limit=args.limit)
