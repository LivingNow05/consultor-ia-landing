import re

with open("js/geo-personalization.js", "r", encoding="utf-8") as f:
    js = f.read()

# Add meta tags update and dyn-country update
new_js = """    // 4. Actualizar el DOM usando clases para actualizar múltiples elementos
    document.querySelectorAll('.dyn-city').forEach(el => el.textContent = data.city);
    document.querySelectorAll('.dyn-currency').forEach(el => el.textContent = data.currency);
    document.querySelectorAll('.dyn-testimonial').forEach(el => el.textContent = data.testimonial);
    document.querySelectorAll('.dyn-company').forEach(el => el.textContent = data.company);
    document.querySelectorAll('.dyn-price').forEach(el => el.textContent = data.price);
    
    // Country capitalization
    const formattedCountry = toTitleCase(countryStr);
    document.querySelectorAll('.dyn-country').forEach(el => el.textContent = formattedCountry || 'Tu País');

    // Update Meta Tags and Title
    document.title = `Automatización de WhatsApp Inteligente en ${data.city}`;
    
    const metaDesc = document.querySelector('meta[name="description"]');
    if(metaDesc) metaDesc.setAttribute('content', `Implementamos tu Chatbot Corporativo en ${data.city}.`);
    
    const metaGeo = document.querySelector('meta[name="geo.placename"]');
    if(metaGeo) metaGeo.setAttribute('content', data.city);
    
    const metaOgTitle = document.querySelector('meta[property="og:title"]');
    if(metaOgTitle) metaOgTitle.setAttribute('content', `Automatización de Ventas en ${data.city}`);
    
    const metaTwitterTitle = document.querySelector('meta[name="twitter:title"]');
    if(metaTwitterTitle) metaTwitterTitle.setAttribute('content', `Automatización de Ventas en ${data.city}`);
"""

js = js.replace("""    // 4. Actualizar el DOM usando clases para actualizar múltiples elementos
    document.querySelectorAll('.dyn-city').forEach(el => el.textContent = data.city);
    document.querySelectorAll('.dyn-currency').forEach(el => el.textContent = data.currency);
    document.querySelectorAll('.dyn-testimonial').forEach(el => el.textContent = data.testimonial);
    document.querySelectorAll('.dyn-company').forEach(el => el.textContent = data.company);
    document.querySelectorAll('.dyn-price').forEach(el => el.textContent = data.price);""", new_js)

with open("js/geo-personalization.js", "w", encoding="utf-8") as f:
    f.write(js)

print("JS updated.")
