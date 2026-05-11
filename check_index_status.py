#!/usr/bin/env python3
"""
check_index_status.py
Consulta el estado de indexación de todas las URLs del sitio
usando la Google Search Console URL Inspection API.

USO:
  python3 check_index_status.py              # Audita todas las URLs
  python3 check_index_status.py --limit 50   # Solo las primeras 50
  python3 check_index_status.py --only-errors # Solo muestra las no indexadas
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime

sys.path.append('/Users/anthony/.gemini/antigravity/skills/google-indexing-api/scripts')

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import requests
except ImportError:
    print("❌ Dependencias faltantes. Ejecuta: pip install google-auth google-auth-oauthlib requests")
    sys.exit(1)

# ─── CONFIG ────────────────────────────────────────────────
SITE_URL        = "https://consultor-ia.com.co/"
INSPECTION_URL  = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
SCOPES          = ["https://www.googleapis.com/auth/webmasters.readonly"]
SECRETS_FILE    = "client_secret_225332237034-80flchf9i185nshspr3e7q0nlj5sjck7.apps.googleusercontent.com.json"
TOKEN_FILE      = "token_inspection.json"   # Token separado para no pisar el de Indexing
URL_LIST_FILE   = "all_urls.txt"
REPORT_FILE     = "index_status_report.json"
DELAY           = 0.3   # segundos entre consultas (~3 req/s, bien bajo el límite de 600/min)
# ───────────────────────────────────────────────────────────

# Mapeo de estados de GSC a iconos (API puede devolver en inglés o español)
STATUS_ICON = {
    # Inglés
    "PASS":    "✅",
    "INDEXED": "✅",
    "NEUTRAL": "🔄",
    "FAIL":    "❌",
    # Razones en español (coverageState)
    "Enviada e indexada":                        "✅",
    "Indexada, no enviada en sitemap":            "✅",
    "Descubierta: actualmente sin indexar":       "🔄",
    "Rastreada: actualmente sin indexar":         "🔄",
    "Duplicado sin URL canónica seleccionada":    "⚠️",
    "Excluido por la etiqueta 'noindex'": "🚫",
    "Bloqueado por robots.txt":                  "🚫",
    "Bloqueado por acceso no permitido":          "🔒",
    "No encontrado (404)":                        "💀",
    "Error del servidor (5xx)":                   "🔥",
    "Redireccionamiento":                         "↩️",
    "Página con redireccionamiento":              "↩️",
    "UNKNOWN":   "❓",
    "API_ERROR": "🔥",
}

def get_icon(verdict, reason):
    """Devuelve el ícono correcto según verdict o reason."""
    if verdict in ("PASS", "INDEXED") or "indexada" in reason.lower():
        return "✅"
    if verdict == "NEUTRAL" or "sin indexar" in reason.lower() or "descubierta" in reason.lower():
        return "🔄"
    if verdict == "FAIL" or "error" in reason.lower() or "no encontrado" in reason.lower():
        return "❌"
    if "bloqueado" in reason.lower() or "robots" in reason.lower():
        return "🚫"
    return STATUS_ICON.get(verdict, STATUS_ICON.get(reason, "❓"))



def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(SECRETS_FILE):
                print(f"❌ No se encontró: {SECRETS_FILE}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    return creds


def inspect_url(url, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = {
        "inspectionUrl": url,
        "siteUrl": SITE_URL,
        "languageCode": "es"
    }
    resp = requests.post(INSPECTION_URL, headers=headers, json=body)
    return resp.status_code, resp.json()


def run(limit=None, only_errors=False):
    # Cargar URLs
    if not os.path.exists(URL_LIST_FILE):
        print(f"❌ No se encontró {URL_LIST_FILE}. Ejecuta primero generate_sitemap.py")
        sys.exit(1)

    with open(URL_LIST_FILE) as f:
        urls = [u.strip() for u in f if u.strip()]
    if limit:
        urls = urls[:limit]

    total = len(urls)
    print(f"\n🔍 Auditando {total} URLs en {SITE_URL}")
    print(f"   Cuota usada: {total}/2000 diarias disponibles\n")

    creds = get_credentials()
    creds.refresh(Request())
    token = creds.token

    results = []
    counts = {}
    
    for i, url in enumerate(urls, 1):
        # Refrescar token cada 100 peticiones
        if i % 100 == 1 and i > 1:
            creds.refresh(Request())
            token = creds.token

        http_status, data = inspect_url(url, token)

        if http_status != 200:
            verdict = "API_ERROR"
            reason = data.get("error", {}).get("message", "?")[:80]
            icon = "🔥"
        else:
            inspection = data.get("inspectionResult", {})
            index_result = inspection.get("indexStatusResult", {})
            verdict = index_result.get("verdict", "UNKNOWN")
            reason = index_result.get("coverageState", "")
            icon = get_icon(verdict, reason)

        counts[verdict] = counts.get(verdict, 0) + 1
        entry = {"url": url, "verdict": verdict, "reason": reason, "icon": icon}
        results.append(entry)

        # Mostrar en consola
        show = True
        if only_errors and verdict == "INDEXED":
            show = False
        if show:
            short_url = url.replace("https://consultor-ia.com.co", "")
            print(f"[{i:03d}/{total}] {icon} {short_url}")
            if reason and verdict != "INDEXED":
                print(f"           → {reason}")

        time.sleep(DELAY)

    # ─── REPORTE FINAL ────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"📊 REPORTE FINAL — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    for verdict, count in sorted(counts.items(), key=lambda x: -x[1]):
        icon = STATUS_ICON.get(verdict, "❓")
        print(f"  {icon} {verdict:<45} {count:>4} páginas")
    print(f"{'='*60}")
    print(f"  Total auditado: {total} URLs\n")

    # Guardar JSON completo
    report = {
        "generated_at": datetime.now().isoformat(),
        "site": SITE_URL,
        "total": total,
        "summary": counts,
        "results": results
    }
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"📄 Reporte completo guardado en: {REPORT_FILE}\n")

    # Lista de URLs con problemas para fácil acceso
    problematic = [r for r in results if r["verdict"] != "INDEXED"]
    if problematic:
        prob_file = "urls_with_issues.txt"
        with open(prob_file, "w") as f:
            for r in problematic:
                f.write(f"{r['icon']} {r['verdict']} | {r['url']} | {r['reason']}\n")
        print(f"⚠️  {len(problematic)} URLs con problemas exportadas a: {prob_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audita el estado de indexación en GSC")
    parser.add_argument("--limit", type=int, default=None, help="Limita el número de URLs a auditar")
    parser.add_argument("--only-errors", action="store_true", help="Solo muestra URLs no indexadas o con errores")
    args = parser.parse_args()
    run(limit=args.limit, only_errors=args.only_errors)
