const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  // Try loading directly via file:// URL to avoid needing a web server
  const url = 'file:///Users/anthony/Downloads/consultor-ia.com.co/dist/chatbot-whatsapp-para-restaurantes/colombia/bogota/index.html';
  console.log(`Navigating to ${url}`);
  
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    
    // Take a full page screenshot
    await page.screenshot({ path: 'screenshot_programatic.png', fullPage: true });
    console.log('Screenshot saved to screenshot_programatic.png');
    
    // Extract information about the CTAs
    const ctas = await page.$$eval('a[href*="wa.me"], button', els => els.map(el => ({
      text: el.innerText,
      href: el.href || null,
      classes: el.className,
      rect: el.getBoundingClientRect()
    })));
    
    console.log('CTAs found:', JSON.stringify(ctas, null, 2));
    
  } catch (e) {
    console.error('Error during QA:', e);
  } finally {
    await browser.close();
  }
})();
