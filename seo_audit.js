const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
    console.log("Iniciando auditoría SEO Evolution Expert...");
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        viewport: { width: 1280, height: 800 },
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    
    const page = await context.newPage();
    const url = 'https://consultor-ia.com.co/';
    
    console.log(`\n--- Auditando: ${url} ---`);
    const start = Date.now();
    const response = await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    const loadTime = ((Date.now() - start) / 1000).toFixed(2);
    
    console.log(`\n1. RENDIMIENTO BÁSICO`);
    console.log(`Status Code: ${response.status()}`);
    console.log(`Load Time: ${loadTime}s`);
    
    console.log(`\n2. SXO (Visibilidad de CTAs Above the Fold)`);
    const ctas = await page.evaluate(() => {
        const buttons = Array.from(document.querySelectorAll('a, button'));
        return buttons.map(b => {
            return { el: b, rect: b.getBoundingClientRect(), text: (b.innerText || '').toLowerCase() };
        }).filter(b => {
            return b.rect.top >= 0 && b.rect.top <= window.innerHeight && b.rect.height > 0 && 
                   (b.text.includes('demo') || b.text.includes('cotizar') || b.text.includes('agendar') || b.text.includes('contactar') || b.text.includes('whatsapp') || b.text.includes('iniciar'));
        }).map(b => ({text: b.el.innerText.trim().replace(/\\n/g, ' '), top: Math.round(b.rect.top)}));
    });
    console.log(`Above the fold CTAs encontrados: ${ctas.length}`);
    ctas.forEach(c => console.log(` - '${c.text}' en y=${c.top}px`));
    
    console.log(`\n3. SXO (Elementos Fijos/Pop-ups Obstructivos)`);
    const popups = await page.evaluate(() => {
        const els = Array.from(document.querySelectorAll('*'));
        return els.filter(el => {
            const style = window.getComputedStyle(el);
            return (style.position === 'fixed' || style.position === 'sticky') && parseInt(style.zIndex) > 10;
        }).map(el => {
            let id = el.id ? '#' + el.id : '';
            let classes = el.className && typeof el.className === 'string' ? '.' + el.className.split(' ').join('.') : '';
            return el.tagName.toLowerCase() + id + classes;
        });
    });
    console.log(`Elementos Fixed/Sticky encontrados (posibles popups): ${popups.length}`);
    popups.slice(0, 3).forEach(p => console.log(` - ${p}`));
    
    console.log(`\n4. AIO/AEO (Estructura de Datos y Entidades - Schema.org)`);
    const schemas = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(s => s.innerText);
    });
    console.log(`JSON-LD Schemas encontrados: ${schemas.length}`);
    schemas.forEach(s => {
        try {
            const schemaJson = JSON.parse(s);
            const schemaType = schemaJson['@type'] || 'Unknown';
            console.log(` - Schema Type: ${schemaType}`);
            if (schemaType === 'FAQPage' && schemaJson.mainEntity) {
                console.log(`   > FAQ Items: ${schemaJson.mainEntity.length}`);
            }
            if (schemaType === 'Organization' && schemaJson.sameAs) {
                console.log(`   > sameAs links: ${schemaJson.sameAs}`);
            }
        } catch (e) {
            console.log(` - Could not parse schema: ${s.substring(0, 50)}...`);
        }
    });
    
    console.log(`\n5. AEO (Pirámide Invertida - Respuestas Directas H2/H3)`);
    const answers = await page.evaluate(() => {
        const headings = Array.from(document.querySelectorAll('h2, h3'));
        let results = [];
        headings.forEach(h => {
            let nextEl = h.nextElementSibling;
            // Buscar si el siguiente elemento es un P
            while(nextEl && nextEl.tagName !== 'P' && nextEl.tagName !== 'DIV' && nextEl.tagName !== 'UL') {
                if(nextEl.tagName === 'H2' || nextEl.tagName === 'H3') break;
                nextEl = nextEl.nextElementSibling;
            }
            if (nextEl && nextEl.tagName === 'P') {
                const words = nextEl.innerText.split(' ').length;
                results.push({heading: h.innerText.substring(0, 40).replace(/\\n/g, ' '), words: words});
            }
        });
        return results;
    });
    console.log(`H2/H3 seguidos directamente por un párrafo (candidatos AEO): ${answers.length}`);
    answers.slice(0, 5).forEach(a => console.log(` - "${a.heading}..." (Longitud: ${a.words} palabras)`));
    
    console.log(`\n6. AEO (Formatos Altamente Extraíbles)`);
    const lists = await page.evaluate(() => document.querySelectorAll("ul, ol").length);
    const tables = await page.evaluate(() => document.querySelectorAll("table").length);
    console.log(`Listas (ul/ol) encontradas: ${lists} | Tablas HTML encontradas: ${tables}`);
    
    console.log(`\n7. SXO / First-Party Data (Captura de Leads)`);
    const forms = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('form')).map(f => {
            const inputs = Array.from(f.querySelectorAll('input, select, textarea')).map(i => i.type || i.tagName.toLowerCase());
            return inputs;
        });
    });
    console.log(`Formularios encontrados: ${forms.length}`);
    forms.forEach((f, i) => console.log(` - Formulario ${i+1} campos: ${f.join(', ')}`));
    
    await browser.close();
    console.log("\nAuditoría finalizada.");
})();
