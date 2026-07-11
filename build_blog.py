import json
import os
import shutil
import re

BLOG_CATEGORY_TAGS = {
    'ia-para-restaurantes': 'Restaurantes',
    'ia-para-salones-de-belleza': 'Estética',
    'ia-para-salud': 'Salud',
    'ia-para-hoteles': 'Hotelería',
    'chatbot-whatsapp-para-inmobiliarias': 'Inmobiliaria',
    'ia-para-retail': 'Retail',
    'precios-agente-ia-latam': 'Precios',
    'como-implementar-agente-ia': 'Implementación',
    'agente-ia-vs-chatbot': 'Tecnología',
    'casos-exito-ia-pymes': 'Casos de Éxito',
    'chatbot-whatsapp': 'Automatización',
    'chatbot-whatsapp-para-empresas': 'Corporativo',
    'click-to-whatsapp-ads-ia': 'Publicidad',
    'nuevas-reglas-meta-chatbot-whatsapp-2026': 'Normativa',
    'whatsapp-corporativo-ia-ventas': 'Ventas',
    'chatbot-whatsapp-notas-de-voz': 'Notas de Voz',
    'agentes-autonomos-ia-whatsapp': 'Agentes IA',
    'precios-whatsapp-business-api-2026': 'Costos',
    'calificacion-leads-whatsapp-ia': 'Leads',
    'embudo-de-ventas-whatsapp-ia': 'Embudos',
    'whatsapp-flows-ia-ventas': 'WhatsApp Flows'
}

def calculate_reading_time(slug):
    filepath = f"dist/blog/{slug}/index.html"
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            text = re.sub(r'<[^>]+>', '', content)
            words = len(text.split())
            minutes = max(1, round(words / 200))
            return minutes
        except Exception as e:
            print(f"Error calculating reading time for {slug}: {e}")
    return 5

def build_blog_index():
    # Cargar blogs publicados
    blogs_file = 'data/published_blogs.json'
    if not os.path.exists(blogs_file):
        blogs = []
    else:
        with open(blogs_file, 'r', encoding='utf-8') as f:
            blogs = json.load(f)
            
    # Ordenar por fecha (más reciente primero)
    blogs.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Construir tarjetas HTML
    cards_html = ""
    for blog in blogs:
        slug = blog.get('slug', '')
        tag_text = BLOG_CATEGORY_TAGS.get(slug, blog.get('category', 'Negocios'))
        minutes = calculate_reading_time(slug)
        card = f"""
        <a href="/blog/{slug}/" class="blog-card-link bg-white dark:bg-zinc-900 rounded-3xl border border-gray-border dark:border-zinc-800 shadow-sm transition-all duration-300 group flex flex-col justify-between overflow-hidden">
            <div class="h-48 relative overflow-hidden">
                <img src="{blog.get('image', '/images/og-home.webp')}" alt="{blog.get('title', '')}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                <div class="absolute inset-0 bg-brand/10 group-hover:bg-transparent transition-colors z-10"></div>
                <div class="absolute top-4 left-4 bg-brand/90 dark:bg-brand-light/90 text-white dark:text-zinc-950 text-[10px] font-bold uppercase tracking-wider px-3 py-1 rounded-full z-20">
                    {tag_text}
                </div>
            </div>
            <div class="p-8 flex-1 flex flex-col justify-between">
                <div>
                    <span class="text-xs font-normal text-zinc-400 dark:text-zinc-500 uppercase tracking-widest flex items-center gap-1.5 mb-3">
                        <i class="far fa-clock text-xs"></i> Lectura: {minutes} min
                    </span>
                    <h2 class="text-xl font-header font-bold mb-3 group-hover:text-brand dark:group-hover:text-brand-light transition-colors">{blog['title']}</h2>
                    <p class="text-zinc-600 dark:text-zinc-400 mb-4 text-sm line-clamp-3">{blog.get('description', '')}</p>
                </div>
                <div class="text-brand dark:text-brand-light font-normal text-sm flex items-center gap-2 group-hover:gap-3 transition-all mt-auto font-semibold">Leer artículo <i class="fas fa-arrow-right"></i></div>
            </div>
        </a>
        """
        cards_html += card
        
    if not blogs:
        cards_html = '<p class="text-gray-500 dark:text-gray-400 text-center w-full col-span-full">Aún no hay artículos publicados. ¡Vuelve pronto!</p>'

    # Cargar template
    with open('templates/blog.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Reemplazar placeholder
    # Asumimos que podemos inyectarlo reemplazando todo lo que esté entre los marcadores <!-- BLOG_CARDS --> si existen,
    # o si no, podemos usar un marcador.
    if '<!-- BLOG_CARDS -->' in html:
        part1, rest = html.split('<!-- BLOG_CARDS_START -->', 1)
        _, part2 = rest.split('<!-- BLOG_CARDS_END -->', 1)
        final_html = part1 + "<!-- BLOG_CARDS_START -->\n" + cards_html + "\n<!-- BLOG_CARDS_END -->" + part2
    else:
        # En templates/blog.html hay una grilla: <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        # Vamos a buscar eso y reemplazar su contenido
        grid_start = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">'
        if grid_start in html:
            parts = html.split(grid_start)
            # Find the closing </div> for the grid
            rest = parts[1]
            end_div_idx = rest.find('</div>\n            </div>\n        </section>')
            if end_div_idx != -1:
                final_html = parts[0] + grid_start + "\n" + cards_html + "\n" + rest[end_div_idx:]
            else:
                print("Error: No se encontró el cierre de la grilla en blog.html")
                return
        else:
            print("Error: No se encontró la grilla en blog.html")
            return

    # Reemplazar footer y variables de WhatsApp
    import urllib.parse
    wa_num = "573151206985"
    wa_msg = "Hola, vengo del blog. Me gustaría más información sobre sus servicios de IA."
    wa_msg_encoded = urllib.parse.quote(wa_msg)
    
    try:
        with open('templates/home.html', 'r', encoding='utf-8') as f:
            home_template = f.read()
            footer = home_template.split('<footer')[1].split('</footer>')[0]
            footer = '<footer' + footer + '</footer>'
    except Exception as e:
        print("Error extract footer", e)
        footer = ""

    final_html = final_html.replace('{FOOTER_HTML}', footer)
    final_html = final_html.replace('{WA_NUMERO}', wa_num)
    final_html = final_html.replace('{WA_MENSAJE_ENCODED}', wa_msg_encoded)

    # Escribir en dist/blog/index.html
    os.makedirs('dist/blog', exist_ok=True)
    with open('dist/blog/index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"Blog index construido con {len(blogs)} artículos.")

if __name__ == '__main__':
    build_blog_index()
