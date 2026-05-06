import os
import re

with open("build.py", "r", encoding="utf-8") as f:
    content = f.read()

agencia_func = """
def build_agencia_pages(data, footer_html, mega_menu_html, urls):
    import os
    from urllib.parse import quote
    
    with open(os.path.join(SRC_DIR, "agencia.html"), "r", encoding="utf-8") as f:
        agencia_template = f.read()
        
    ciudades_colombia = set()
    for row in data:
        if row.get('País') == 'Colombia' and row.get('Estado') == 'PUBLICAR':
            ciudades_colombia.add(row.get('Ciudad'))
            
    for ciudad in ciudades_colombia:
        # Encuentra una fila representativa de esta ciudad para usar sus variables genéricas
        row = next(r for r in data if r.get('Ciudad') == ciudad and r.get('País') == 'Colombia')
        
        ciudad_slug = row.get('Ciudad_Slug', '')
        if not ciudad_slug: continue
        
        url_final = f"/agencia-de-inteligencia-artificial-en-{ciudad_slug}"
        
        out_html = agencia_template
        
        wa_mensaje = f"Hola, busco una Agencia de IA en {ciudad}"
        wa_encoded = quote(wa_mensaje)
        
        replacements = {
            '{FOOTER_HTML}': footer_html,
            '{MEGA_MENU}': mega_menu_html,
            '{H1}': f"Agencia de Inteligencia Artificial en {ciudad}",
            '{H1_HTML}': f'Agencia de <span class="text-brand dark:text-brand-light block mt-2">Inteligencia Artificial en {ciudad}<span class="typewriter-cursor"></span></span>',
            '{TITLE_SEO}': f"Agencia de Inteligencia Artificial en {ciudad} 2026 | Consultor IA",
            '{META_DESCRIPTION}': f"Tu Agencia de Inteligencia Artificial en {ciudad}. Implementamos automatizaciones, agentes virtuales y consultoría estratégica para escalar tu negocio.",
            '{CIUDAD}': ciudad,
            '{PAIS}': row.get('País', ''),
            '{CODIGO_PAIS}': row.get('Codigo_Pais', 'co'),
            '{URL_FINAL}': url_final + "/",
            '{WA_NUMERO}': '573132644262',
            '{WA_MENSAJE_ENCODED}': wa_encoded,
            '{PRECIO_BAJO}': row.get('Precio_Bajo', '800.000'),
            '{PRECIO_MEDIO}': row.get('Precio_Medio', '1.800.000'),
            '{PRECIO_ALTO}': row.get('Precio_Alto', '3.500.000'),
            '{MONEDA}': row.get('Moneda', 'COP')
        }
        
        for k, v in replacements.items():
            out_html = out_html.replace(k, str(v))
            
        # Limpiar variables no reemplazadas
        out_html = re.sub(r'{.*?}', '', out_html)
            
        page_dir = os.path.join(DIST_DIR, url_final.strip('/'))
        os.makedirs(page_dir, exist_ok=True)
        
        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(out_html)
            
        urls.append(f"https://consultor-ia.com.co{url_final}/")
        print(f"Generated Agencia page for {ciudad}")

"""

# Insert function before if __name__ == "__main__":
content = content.replace('if __name__ == "__main__":', agencia_func + '\nif __name__ == "__main__":')

# Insert call inside build() just before print(f"Build complete!...
build_call = '    build_agencia_pages(data, footer_html, mega_menu_html, urls)\n    print(f"Build complete!'
content = content.replace('    print(f"Build complete!', build_call)

with open("build.py", "w", encoding="utf-8") as f:
    f.write(content)

print("build.py updated successfully.")
