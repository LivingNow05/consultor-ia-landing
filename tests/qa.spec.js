const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('Consultor IA - Demo Interactiva Booking QA', () => {
    
    test('Debe agendar una cita interactiva correctamente usando el calendario y el chat del agente', async ({ page }) => {
        // Cargar el archivo compilado local
        const filePath = path.resolve(__dirname, '../dist/chatbot-whatsapp-para-academias-cursos/argentina/buenos-aires/index.html');
        const fileUrl = `file://${filePath}`;
        
        console.log(`Navigating to: ${fileUrl}`);
        await page.goto(fileUrl);
        
        // Esperar que cargue el DOM
        await page.waitForLoadState('domcontentloaded');
        
        // 1. Verificar presencia de la Demo
        const demoSection = page.locator('#demo-interactiva');
        await expect(demoSection).toBeVisible();
        
        // 2. Interactuar con el Calendario: seleccionar el día 22 (Lunes)
        // Buscamos el botón de día en la grilla que tenga el número 22
        const day22Button = page.locator('#calendar-days-grid button').getByText(/^22$/, { exact: true });
        await expect(day22Button).toBeVisible();
        await day22Button.click();
        
        // 3. Verificar disponibilidad listada en el contenedor de horas para el día seleccionado
        const selectedDayLabel = page.locator('#selected-day-label');
        await expect(selectedDayLabel).toContainText('lunes, 22 de junio');
        
        // 4. Localizar dinámicamente el primer botón de hora libre (que no tenga clase pointer-events-none)
        const slotButton = page.locator('#time-slots-container button:not(.pointer-events-none)').first();
        await expect(slotButton).toBeVisible();
        const slotText = (await slotButton.innerText()).trim();
        console.log(`Día 22 seleccionado. Horario libre detectado dinámicamente: ${slotText}`);
        
        // 5. Hacer clic en el slot libre para autocompletar el input del chat
        await slotButton.click();
        
        // Verificar que el input del chat contenga la cadena autocompletada
        const chatInput = page.locator('#demo-chat-input');
        await expect(chatInput).toHaveValue(new RegExp(slotText));
        
        // 6. Enviar el mensaje del usuario
        const sendBtn = page.locator('#demo-chat-send-btn');
        await sendBtn.click();
        
        // 7. Esperar a que el bot procese el mensaje y responda (simulación de tipeo de 3 segundos)
        const chatBody = page.locator('#demo-chat-body');
        
        // Esperar a que aparezca la respuesta del bot (el bot debe solicitar el nombre y correo)
        await page.waitForTimeout(4000); // 4 segundos de espera para que termine de escribir
        
        // El último mensaje del cuerpo del chat debe ser la respuesta del asistente
        const lastMessage = chatBody.locator('div').last();
        await expect(lastMessage).toContainText(/(nombre|correo|email|disponible)/i);
        
        // Verificar que no diga "ocupado" ni "no está disponible"
        const lastMessageText = await lastMessage.innerText();
        console.log(`Respuesta 1 del Agente IA: "${lastMessageText}"`);
        expect(lastMessageText.toLowerCase()).not.toContain('ocupado');
        expect(lastMessageText.toLowerCase()).not.toContain('no está disponible');
        
        // 8. Enviar el nombre y correo para confirmar la cita
        await chatInput.fill('Mi nombre es Juan Pérez y mi correo es juan@gmail.com');
        await sendBtn.click();
        
        // Esperar a que el bot procese la confirmación (tipeo)
        await page.waitForTimeout(4000);
        
        // 9. Verificar que se muestre la confirmación y el ticket de reserva a la derecha
        const ticketName = page.locator('#ticket-name');
        await expect(ticketName).toHaveText('Juan Pérez');
        
        const ticketTime = page.locator('#ticket-time');
        await expect(ticketTime).toHaveText(slotText);
        
        const ticketDate = page.locator('#ticket-date');
        await expect(ticketDate).toContainText('22 de junio');
        
        console.log('✅ Test de flujo interactivo de agendamiento completado con éxito!');
    });
});
