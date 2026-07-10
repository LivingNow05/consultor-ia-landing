document.addEventListener('DOMContentLoaded', function() {
    // 1. Extraer ciudad del pathname
    const path = window.location.pathname;
    // Asume un patrón como /automatizacion-whatsapp-ia/pais/ciudad/
    // Ejemplo: /automatizacion-whatsapp-ia/mexico/monterrey/
    const parts = path.split('/').filter(Boolean);
    
    let cityStr = 'tu ciudad';
    let countryStr = '';
    
    if (parts.length >= 3 && parts[0] === 'automatizacion-whatsapp-ia') {
        countryStr = parts[1].toLowerCase();
        cityStr = parts[2].toLowerCase(); 
    } else if (parts.length === 2 && parts[0] === 'automatizacion-whatsapp-ia') {
        cityStr = parts[1].toLowerCase();
    }

    // Formatear ciudad
    const toTitleCase = (str) => {
        if(str === 'tu ciudad') return str;
        return str.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    };
    
    let formattedCity = toTitleCase(cityStr);
    
    // Tildes comunes para mejorar presentación
    const tildes = {
        'Bogota': 'Bogotá',
        'Medellin': 'Medellín',
        'Cancun': 'Cancún',
        'Queretaro': 'Querétaro',
        'Merida': 'Mérida',
        'San Jose Cr': 'San José',
        'Panama': 'Panamá',
        'Cordoba Ar': 'Córdoba'
    };
    if (tildes[formattedCity]) formattedCity = tildes[formattedCity];

    // Moneda y Precio por país (aproximado)
    let currency = 'USD';
    let price = '499';
    if (countryStr === 'colombia') { currency = 'COP'; price = '1.800.000'; }
    else if (countryStr === 'mexico') { currency = 'MXN'; price = '9.500'; }
    else if (countryStr === 'peru') { currency = 'PEN'; price = '1.900'; }
    else if (countryStr === 'chile') { currency = 'CLP'; price = '450.000'; }
    else if (countryStr === 'argentina') { currency = 'ARS'; price = '500.000'; }

    const data = {
        city: formattedCity,
        currency: currency,
        company: `Tu Empresa en ${formattedCity}`,
        testimonial: `"Nuestra atención al cliente en ${formattedCity} mejoró en un 40% gracias a la automatización inteligente." - Negocio Local`,
        price: price
    };

    // 4. Actualizar el DOM usando clases para actualizar múltiples elementos
    document.querySelectorAll('.dyn-city').forEach(el => el.textContent = data.city);
    document.querySelectorAll('.dyn-currency').forEach(el => el.textContent = data.currency);
    document.querySelectorAll('.dyn-testimonial').forEach(el => el.textContent = data.testimonial);
    document.querySelectorAll('.dyn-company').forEach(el => el.textContent = data.company);
    document.querySelectorAll('.dyn-price').forEach(el => el.textContent = data.price);

});
