import asyncio
from playwright.async_api import async_playwright
import json
import time

async def audit_page(url, page_type):
    print(f"\\n--- Auditing {page_type}: {url} ---")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        start_time = time.time()
        try:
            response = await page.goto(url, wait_until='networkidle', timeout=15000)
            load_time = time.time() - start_time
            print(f"Load Time: {load_time:.2f}s")
            print(f"Status Code: {response.status}")
        except Exception as e:
            print(f"Error loading {url}: {e}")
            await browser.close()
            return
            
        # 1. SXO: Above the fold CTAs
        ctas = await page.evaluate('''() => {
            const buttons = Array.from(document.querySelectorAll('a, button'));
            return buttons.filter(b => {
                const rect = b.getBoundingClientRect();
                const text = b.innerText.toLowerCase();
                return rect.top >= 0 && rect.top <= window.innerHeight && rect.height > 0 && 
                       (text.includes('demo') || text.includes('cotizar') || text.includes('agendar') || text.includes('contactar') || text.includes('whatsapp'));
            }).map(b => ({text: b.innerText, top: b.getBoundingClientRect().top}));
        }''')
        print(f"Above the fold CTAs: {len(ctas)}")
        for c in ctas:
            print(f" - '{c['text']}' at y={c['top']:.0f}px")
            
        # 2. SXO: Intrusive Pop-ups / Sticky elements
        popups = await page.evaluate('''() => {
            const els = Array.from(document.querySelectorAll('*'));
            return els.filter(el => {
                const style = window.getComputedStyle(el);
                return (style.position === 'fixed' || style.position === 'sticky') && style.zIndex > 10;
            }).map(el => el.tagName + '#' + el.id + '.' + el.className.split(' ').join('.'));
        }''')
        print(f"Fixed/Sticky elements (potential popups/banners): {len(popups)}")
        for p in popups[:3]:
            print(f" - {p}")
            
        # 3. AIO / AEO: Schema.org JSON-LD
        schemas = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(s => s.innerText);
        }''')
        print(f"JSON-LD Schemas found: {len(schemas)}")
        for s in schemas:
            try:
                schema_json = json.loads(s)
                schema_type = schema_json.get('@type', 'Unknown')
                print(f" - Schema Type: {schema_type}")
                if schema_type == 'FAQPage':
                    questions = schema_json.get('mainEntity', [])
                    print(f"   > FAQ Items: {len(questions)}")
                if schema_type == 'Organization':
                    print(f"   > sameAs links: {schema_json.get('sameAs', 'None')}")
            except:
                print(" - Could not parse schema")
                
        # 4. AEO: Inverted Pyramid / Direct answers (H2/H3 followed by short paragraph)
        answers = await page.evaluate('''() => {
            const headings = Array.from(document.querySelectorAll('h2, h3'));
            let results = [];
            headings.forEach(h => {
                const nextEl = h.nextElementSibling;
                if (nextEl && nextEl.tagName === 'P') {
                    const words = nextEl.innerText.split(' ').length;
                    results.push({heading: h.innerText.substring(0, 30) + '...', words: words});
                }
            });
            return results;
        }''')
        print(f"H2/H3 directly followed by paragraph: {len(answers)}")
        for a in answers[:3]:
            print(f" - {a['heading']} (Length: {a['words']} words)")
            
        # 5. AEO: Highly extractable formats (Lists, Tables)
        lists = await page.evaluate('() => document.querySelectorAll("ul, ol").length')
        tables = await page.evaluate('() => document.querySelectorAll("table").length')
        print(f"Lists found: {lists} | Tables found: {tables}")
        
        # 6. SXO/Retention: Forms for First-Party Data
        forms = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('form')).map(f => {
                const inputs = Array.from(f.querySelectorAll('input, select, textarea')).map(i => i.type || i.tagName.toLowerCase());
                return inputs;
            });
        }''')
        print(f"Forms found: {len(forms)}")
        for f in forms:
            print(f" - Form fields: {f}")
            
        await browser.close()

async def main():
    urls = [
        "https://consultor-ia.com.co/",
        "https://consultor-ia.com.co/chatbot-whatsapp-para-restaurantes/colombia/medellin/"
    ]
    for u in urls:
        await audit_page(u, "Page")

if __name__ == "__main__":
    asyncio.run(main())
