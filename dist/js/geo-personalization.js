document.addEventListener('DOMContentLoaded', function() {
    // 1. Extraer ciudad del pathname
    const path = window.location.pathname;
    // Asume un patrón como /automatizacion-whatsapp-ia/pais/ciudad/
    // Ejemplo: /automatizacion-whatsapp-ia/mexico/monterrey/
    const parts = path.split('/').filter(Boolean);
    
    let cityStr = 'default';
    if (parts.length >= 3 && parts[0] === 'automatizacion-whatsapp-ia') {
        cityStr = parts[2].toLowerCase(); // Toma 'monterrey' de parts = ['automatizacion-whatsapp-ia', 'mexico', 'monterrey']
    } else if (parts.length === 2 && parts[0] === 'automatizacion-whatsapp-ia') {
        cityStr = parts[1].toLowerCase();
    }

    // 2. Diccionario de datos mock (base de datos geo-personalizada)
    const geoData = {
        'monterrey': {
            city: 'Monterrey',
            currency: 'MXN',
            company: 'Industrias Regias',
            savings: '40%',
            testimonial: '"Implementar IA en Monterrey con ellos aumentó nuestras ventas un 40% y redujo tiempos." - Industrias Regias'
        },
        'bogota': {
            city: 'Bogotá',
            currency: 'COP',
            company: 'Comercio Capital',
            savings: '45%',
            testimonial: '"Automatizamos nuestro WhatsApp en Bogotá y bajamos costos un 45% en servicio." - Comercio Capital'
        },
        'lima': {
            city: 'Lima',
            currency: 'PEN',
            company: 'Servicios Andinos',
            savings: '35%',
            testimonial: '"La solución que necesitábamos para escalar en todo Perú, altamente recomendado." - Servicios Andinos'
        },
        'default': {
            city: 'tu ciudad',
            currency: 'USD',
            company: 'Empresa Líder',
            savings: '30%',
            testimonial: '"Nuestra atención al cliente mejoró en un 30% gracias a la automatización inteligente." - Empresa Líder'
        }
    };

    // 3. Obtener los datos de la ciudad (o fallback a default)
    const data = geoData[cityStr] || geoData['default'];

    // 4. Actualizar el DOM usando clases para actualizar múltiples elementos
    document.querySelectorAll('.dyn-city').forEach(el => el.textContent = data.city);
    document.querySelectorAll('.dyn-currency').forEach(el => el.textContent = data.currency);
    document.querySelectorAll('.dyn-testimonial').forEach(el => el.textContent = data.testimonial);
    document.querySelectorAll('.dyn-company').forEach(el => el.textContent = data.company);
    document.querySelectorAll('.dyn-price').forEach(el => el.textContent = '499'); // Podrías añadirlo a geoData si varía

});
