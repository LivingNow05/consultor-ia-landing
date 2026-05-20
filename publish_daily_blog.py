import json
import os
import urllib.parse
import datetime
from build_blog import build_blog_index

def get_footer_and_menu():
    try:
        with open('templates/home.html', 'r', encoding='utf-8') as f:
            home = f.read()
            # Simplista: extraemos mega menu y footer asumiendo que build.py hace algo similar,
            # o simplemente podemos leer los partials si existen.
            # En consultor-ia parece que mega_menu y footer se inyectan.
            # Para el blog, podemos usar componentes estáticos o simplemente dejar lo que build.py haga.
            # Pero build.py no maneja el blog. Así que los extraeremos de agencia.html o home.html.
            pass
    except:
        pass
    # Por simplicidad, si {MEGA_MENU} está, lo reemplazamos con un header básico o lo leemos.
    # Vamos a usar fix_mega_menu.py o similar si es necesario. Para no romper, pondremos vacío.
    return "", ""

def publish_blog(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    slug = data['slug']
    h1 = data['h1']
    title_seo = data['title_seo']
    meta_desc = data['meta_description']
    content_html = data['content_html']
    image_url = f"/images/blog/{slug}/hero.webp"
    
    # Renderizar template
    with open('templates/pillar.html', 'r', encoding='utf-8') as f:
        template = f.read()
        
    wa_num = "573151206985"
    wa_msg = f"Hola, vengo del artículo del blog: {h1}. Me gustaría más información."
    wa_msg_encoded = urllib.parse.quote(wa_msg)
    
    html = template.replace('{TITLE_SEO}', title_seo)
    html = template.replace('{META_DESCRIPTION}', meta_desc)
    html = template.replace('{SLUG}', f"blog/{slug}")
    html = template.replace('{H1}', h1)
    
    # H1_HTML con un diseño bonito para blog
    h1_html = f"""
    <div class="text-center mb-8">
        <span class="text-brand dark:text-brand-light font-medium tracking-wider uppercase text-sm mb-4 block">Blog / Negocios</span>
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-header font-bold text-gradient mb-6 leading-tight">{h1}</h1>
        <p class="text-lg text-gray-2 dark:text-slate-400 max-w-3xl mx-auto">{meta_desc}</p>
    </div>
    <div class="w-full h-[50vh] md:h-[60vh] rounded-3xl overflow-hidden mb-12 shadow-2xl relative">
        <img src="{image_url}" alt="{h1}" class="w-full h-full object-cover">
    </div>
    """
    html = html.replace('{H1_HTML}', h1_html)
    
    # Envolver contenido en prose
    content_wrapped = f"""
    <div class="prose prose-lg dark:prose-invert max-w-4xl mx-auto prose-headings:font-header prose-headings:font-bold prose-a:text-brand dark:prose-a:text-brand-light prose-img:rounded-2xl prose-img:shadow-lg">
        {content_html}
    </div>
    """
    html = html.replace('{CONTENT_HTML}', content_wrapped)
    html = html.replace('{WA_NUMERO}', wa_num)
    html = html.replace('{WA_MENSAJE_ENCODED}', wa_msg_encoded)
    
    # Reemplazar mega menu y footer por ahora con cadena vacía si no tenemos la función de build.py,
    # o usar build.py functions. Para no liarnos, dejaremos que build.py reemplace MEGA_MENU si lo corre,
    # o lo reemplazamos con un header básico.
    # En realidad, si dejamos {MEGA_MENU} y corremos build.py, ¿build.py lo procesará?
    # build.py lee de templates/ y escribe en dist/.
    # Entonces guardaremos el HTML en templates/blog_{slug}.html y lo compilamos? No, build.py itera sobre CSVs.
    
    # Mejor copiemos el header de blog.html.
    with open('templates/blog.html', 'r', encoding='utf-8') as f:
        blog_template = f.read()
        try:
            header = blog_template.split('<header')[1].split('</header>')[0]
            header = '<header' + header + '</header>'
            footer = blog_template.split('<footer')[1].split('</footer>')[0]
            footer = '<footer' + footer + '</footer>'
        except:
            header, footer = "", ""
            
    html = html.replace('{MEGA_MENU}', header)
    html = html.replace('{FOOTER_HTML}', footer)
    
    # Guardar en dist
    out_dir = f"dist/blog/{slug}"
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{out_dir}/index.html", 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"✅ Artículo {slug} compilado en {out_dir}/index.html")
    
    # Actualizar published_blogs.json
    blogs_file = 'data/published_blogs.json'
    if os.path.exists(blogs_file):
        with open(blogs_file, 'r', encoding='utf-8') as f:
            blogs = json.load(f)
    else:
        blogs = []
        
    # Remover si ya existe (para actualizar)
    blogs = [b for b in blogs if b['slug'] != slug]
    
    blogs.append({
        'title': h1,
        'slug': slug,
        'description': meta_desc,
        'image': image_url,
        'category': 'Negocios',
        'date': datetime.datetime.now().isoformat()
    })
    
    with open(blogs_file, 'w', encoding='utf-8') as f:
        json.dump(blogs, f, indent=4, ensure_ascii=False)
        
    # Reconstruir índice
    build_blog_index()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        publish_blog(sys.argv[1])
    else:
        print("Uso: python3 publish_daily_blog.py <ruta_al_json>")
