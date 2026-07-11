const { test, expect } = require('@playwright/test');

test('verificar confirmación de cita en el calendario', async ({ page }) => {
  await page.goto('http://localhost:8000/dist/chatbot-whatsapp-para-restaurantes/colombia/bogota/index.html');

  // Asegurar que estamos al menos 7 días en el futuro haciendo clic en el botón de siguiente
  const nextBtn = page.locator('#calendar-next-btn');
  if (await nextBtn.isVisible()) {
      await nextBtn.click();
      await page.waitForTimeout(500); // Esperar a que la transición ocurra
      
      // Hacemos un segundo clic por seguridad en caso de que sea vista semanal
      await nextBtn.click();
      await page.waitForTimeout(500);
  }

  // Seleccionar directamente un día libre en el calendario
  const diaLibre = page.locator('#calendar-days-grid button:not(.pointer-events-none)').nth(0);
  await diaLibre.waitFor({ state: 'visible' });
  await diaLibre.click();

  // Hacer clic en un horario libre
  const horarioLibre = page.locator('#time-slots-container button:not(.pointer-events-none)').nth(0);
  await horarioLibre.waitFor({ state: 'visible' });
  await horarioLibre.click();

  // Enviar el mensaje
  // Capturar la respuesta del bot desde la red antes de que se parsee y elimine el tag
  const [response] = await Promise.all([
    page.waitForResponse(res => res.url().includes('openrouter.ai') && res.status() === 200, { timeout: 15000 }),
    page.locator('#demo-chat-send-btn').click()
  ]);

  const jsonResponse = await response.json();
  const botMessage = jsonResponse.choices[0].message.content;
  console.log("Respuesta real del bot:", botMessage);

  // Verificar que contiene el texto de confirmación
  const hasConfirmTag = botMessage.includes('[CONFIRMAR_CITA:');
  
  if (!hasConfirmTag) {
    throw new Error('La respuesta del bot no contiene el texto [CONFIRMAR_CITA:');
  }

  // Verificación final del texto
  const textoChat = await page.locator('#demo-chat-body').innerText();
  expect(textoChat).toContain('[CONFIRMAR_CITA:');
});
