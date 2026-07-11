const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.goto('file:///Users/anthony/Downloads/consultor-ia.com.co/dist/chatbot-whatsapp-para-restaurantes/colombia/bogota/index.html');
  await page.setViewportSize({ width: 1280, height: 2800 }); // Large viewport to capture all
  
  // Optional: wait a little for background blobs and fonts
  await page.waitForTimeout(2000);
  
  await page.screenshot({ path: '/Users/anthony/Downloads/consultor-ia.com.co/new_programatic.png', fullPage: true });
  await browser.close();
})();
