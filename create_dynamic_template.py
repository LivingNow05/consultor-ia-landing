import sys
import os

sys.path.append(os.getcwd())
import build

# We will read templates/template.html
with open('templates/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Create dummy row
row = {
    'Ciudad': '<span id="dynamic-city">tu ciudad</span>',
    'Moneda': '<span id="dynamic-currency">USD</span>',
    'Precio_Bajo': '<span id="dynamic-price">499</span>',
    'Industria_Singular': 'negocio',
    'Industria': 'Negocios',
    'Cliente_Negocio': '<span id="dynamic-company">Tu Empresa</span>',
    'País': 'tu país',
    'Demónimo': 'habitantes',
    'Barrios': 'barrios principales',
    'Dolor_Principal': 'perder ventas',
    'Solución_Clave': 'automatizar las respuestas'
}

# We need to fill in the python format string with span tags that the JS can target.
mapping = {
    '{CODIGO_PAIS}': 'es',
    '{TITLE_SEO}': 'Automatización de WhatsApp Inteligente en tu ciudad',
    '{META_DESCRIPTION}': 'Implementamos tu Chatbot Corporativo en tu ciudad.',
    '{KEYWORD_PRINCIPAL}': 'automatizacion de whatsapp',
    '{KEYWORD_SECUNDARIA}': 'chatbot corporativo',
    '{KEYWORD_TERCIARIA}': 'ia generativa',
    '{CIUDAD}': '<span id="dynamic-city" class="dyn-city">tu ciudad</span>',
    '{URL_FINAL}': '/automatizacion-whatsapp-ia/',
    '{H1}': 'Automatización de Ventas en <span id="dynamic-city" class="text-accent underline decoration-4 decoration-accent/30 dyn-city">tu ciudad</span>',
    '{INDUSTRIA_SLUG}': 'default',
    '{MONEDA}': '<span id="dynamic-currency" class="dyn-currency">USD</span>',
    '{BARRIOS}': 'barrios principales',
    '{DOLOR_PRINCIPAL}': 'perder ventas',
    '{SOLUCION_CLAVE}': 'automatizar tus respuestas',
    '{DEMONIMO}': 'habitantes',
    '{CLIENTE_NEGOCIO}': '<span id="dynamic-company">Tu Empresa</span>',
    '{INDUSTRIA_SINGULAR}': 'tu sector',
    '{PRECIO_BAJO}': '<span id="dynamic-price">499</span>',
    '{PAIS}': 'tu país',
    '{EMOJIS_PROBLEMA}': '😞',
    '{EMOJIS_SOLUCION}': '🚀',
    '{ROLES_OBJETIVO}': 'gerentes',
    '{TIEMPO_CONFIGURACION}': 'pocos días',
    '{TESTIMONIOS}': '<blockquote class="italic text-lg text-gray-700 bg-gray-50 p-6 rounded-lg border-l-4 border-accent"><span id="dynamic-testimonial">"Nuestra atención al cliente mejoró en un 30% gracias a la automatización inteligente." - Empresa Líder</span></blockquote>',
    '{PREGUNTAS_FRECUENTES}': '',
    '{TABLA_ROI_HTML}': build.build_roi_table_html(row),
    '{CALCULADORA_ROI_HTML}': build.build_calculadora_html(row),
    '{DEMO_INTERACTIVA_HTML}': build.build_demo_interactiva_html(row),
    '{PRECIOS_HTML}': build.build_precios_seccion_html(row),
    '{ROADMAP_HTML}': build.build_roadmap_html(row),
    '{HERO_VISUAL}': '',
    '{SERVICIOS_CARDS}': '',
    '{CONTENIDO_EEAT}': '',
    '{CIUDADES_HERMANAS}': '',
    '{BLOG_RECOMENDACIONES}': '',
    '{MAPA_HTML}': '' # Leave map empty or generic
}

for key, val in mapping.items():
    html = html.replace(key, str(val))

with open('templates/automatizacion_whatsapp.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated templates/automatizacion_whatsapp.html")
