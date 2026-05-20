import json
import os
import urllib.parse
import datetime
import shutil
from build_blog import build_blog_index

def publish_blog(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    slug = data['slug']
    h1 = data['h1']
    title_seo = data['title_seo']
    meta_desc = data['meta_description']
    content_html = data['content_html']
    image_url = f"/images/blog/{slug}/hero.webp"
    
    # Copiar la imagen a dist/ para que Vercel la sirva
    src_image = f"images/blog/{slug}/hero.webp"
    dist_image_dir = f"dist/images/blog/{slug}"
    if os.path.exists(src_image):
        os.makedirs(dist_image_dir, exist_ok=True)
        shutil.copy2(src_image, f"{dist_image_dir}/hero.webp")
    
    # Renderizar template
    with open('templates/pillar.html', 'r', encoding='utf-8') as f:
        template = f.read()
        
    wa_num = "573151206985"
    wa_msg = f"Hola, vengo del artículo del blog: {h1}. Me gustaría más información."
    wa_msg_encoded = urllib.parse.quote(wa_msg)
    
    html = template.replace('{TITLE_SEO}', title_seo)
    html = html.replace('{META_DESCRIPTION}', meta_desc)
    html = html.replace('{SLUG}', f"blog/{slug}")
    html = html.replace('{H1}', h1)
    
    # En pillar.html, {H1_HTML} está dentro de un <h1>. No podemos inyectar un div ahí.
    html = html.replace('{H1_HTML}', h1)
    
    # Envolver contenido en prose, inyectando la imagen Hero al principio.
    hero_html = f"""
    <div class="w-full h-[40vh] md:h-[50vh] rounded-3xl overflow-hidden mb-12 shadow-2xl relative mt-12 max-w-5xl mx-auto">
        <img src="{image_url}" alt="{h1}" class="w-full h-full object-cover">
    </div>
    """
    
    # A custom Table of Contents or Rich formatting should be part of content_html.
    content_wrapped = f"""
    <section class="py-12 bg-white dark:bg-zinc-950">
        {hero_html}
        <div class="container mx-auto px-4 max-w-4xl">
            <div class="prose prose-lg dark:prose-invert max-w-none prose-headings:font-header prose-headings:font-bold prose-a:text-brand dark:prose-a:text-brand-light prose-img:rounded-2xl prose-img:shadow-lg prose-table:rounded-xl prose-table:overflow-hidden">
                {content_html}
            </div>
        </div>
    </section>
    """
    html = html.replace('{CONTENT_HTML}', content_wrapped)
    # Header y footer
    try:
        with open('templates/blog.html', 'r', encoding='utf-8') as f:
            blog_template = f.read()
            header = blog_template.split('<header')[1].split('</header>')[0]
            header = '<header' + header + '</header>'
            
        with open('templates/home.html', 'r', encoding='utf-8') as f:
            home_template = f.read()
            footer = home_template.split('<footer')[1].split('</footer>')[0]
            footer = '<footer' + footer + '</footer>'
    except Exception as e:
        print("Error extract header/footer", e)
        header, footer = "", ""
            
    html = html.replace('{MEGA_MENU}', header)
    html = html.replace('{FOOTER_HTML}', footer)
    
    # Reemplazar variables de WhatsApp en todo el documento (incluyendo header/footer)
    html = html.replace('{WA_NUMERO}', wa_num)
    html = html.replace('{WA_MENSAJE_ENCODED}', wa_msg_encoded)
    
    # Guardar en dist
    out_dir = f"dist/blog/{slug}"
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{out_dir}/index.html", 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"✅ Artículo {slug} compilado en {out_dir}/index.html")
    
    # Indexar automáticamente en Google
    try:
        url_to_index = f"https://consultor-ia.com.co/blog/{slug}/"
        print(f"🚀 Enviando notificación de indexación para: {url_to_index}")
        
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request as GoogleRequest
        import requests
        
        SCOPES = ["https://www.googleapis.com/auth/indexing"]
        INDEXING_API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        
        if os.path.exists("service-account.json"):
            creds = service_account.Credentials.from_service_account_file(
                "service-account.json", scopes=SCOPES
            )
            creds.refresh(GoogleRequest())
            token = creds.token
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            body = {"url": url_to_index, "type": "URL_UPDATED"}
            response = requests.post(INDEXING_API_URL, headers=headers, json=body)
            
            if response.status_code == 200:
                print(f"✅ Éxito: Google ha recibido la notificación de indexación para: {url_to_index}")
            else:
                print(f"❌ Error al notificar a Google ({response.status_code}): {response.text}")
        else:
            print("⚠️ No se encontró service-account.json, se omite la indexación automática.")
    except Exception as e:
        print(f"⚠️ Error durante la indexación automática: {e}")
    
    # Actualizar published_blogs.json
    blogs_file = 'data/published_blogs.json'
    if os.path.exists(blogs_file):
        with open(blogs_file, 'r', encoding='utf-8') as f:
            blogs = json.load(f)
    else:
        blogs = []
        
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
