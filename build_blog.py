import json
import os
import shutil

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
        card = f"""
        <article class="bg-white dark:bg-zinc-900 rounded-3xl overflow-hidden border border-gray-border dark:border-zinc-800 shadow-sm hover:shadow-xl dark:hover:shadow-[0_8px_30px_-12px_rgba(16,185,129,0.15)] transition-all duration-300 group">
            <div class="h-48 relative overflow-hidden">
                <img src="{blog.get('image', '/images/og-home.webp')}" alt="{blog.get('title', '')}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                <div class="absolute inset-0 bg-brand/10 group-hover:bg-transparent transition-colors z-10"></div>
            </div>
            <div class="p-8">
                <span class="text-xs font-normal text-brand dark:text-brand-light uppercase tracking-wider mb-2 block">{blog.get('category', 'Negocios')}</span>
                <h2 class="text-xl font-header font-bold mb-3 group-hover:text-brand transition-colors"><a href="/blog/{blog['slug']}/">{blog['title']}</a></h2>
                <p class="text-gray-2 dark:text-slate-400 mb-4 text-sm">{blog.get('description', '')}</p>
                <a href="/blog/{blog['slug']}/" class="text-brand dark:text-brand-light font-normal text-sm flex items-center gap-2 group-hover:gap-3 transition-all">Leer artículo <i class="fas fa-arrow-right"></i></a>
            </div>
        </article>
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

    # Escribir en dist/blog/index.html
    os.makedirs('dist/blog', exist_ok=True)
    with open('dist/blog/index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"Blog index construido con {len(blogs)} artículos.")

if __name__ == '__main__':
    build_blog_index()
