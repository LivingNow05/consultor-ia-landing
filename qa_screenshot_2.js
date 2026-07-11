const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.goto('file:///Users/anthony/Downloads/consultor-ia.com.co/dist/automatizacion-whatsapp-dinamica.html');
  await page.setViewportSize({ width: 1280, height: 2800 }); // Large viewport to capture all
  
  // Optional: wait a little for background blobs and fonts
  await page.waitForTimeout(2000);
  
  await page.screenshot({ path: '/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/dynamic_programatic.png', fullPage: true });
  await browser.close();
})();
