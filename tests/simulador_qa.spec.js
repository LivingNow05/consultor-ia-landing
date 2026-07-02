const { test, expect } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

/**
 * QA Automation Test Suite para la landing page de Consultor IA
 * 
 * Este script realiza:
 * 1. Auditoría SEO (Title, Meta Description, Estructura H1 única).
 * 2. Auditoría interactiva del "Simulador de Costo y ROI de App".
 * 3. Verificación de selección de bajo presupuesto (debe mostrar CTA de WhatsApp).
 * 4. Verificación de selección de alto presupuesto (debe mostrar CTA de Calendly).
 * 5. Detección de errores de consola y excepciones de carga.
 */

// Selectores reales mapeados a partir de build.py
const SELECTORS = {
    // Contenedores del Simulador
    resultsScreen: '#app-results-screen',
    ctaScreen: '#app-cta-screen',
    qualifyBtn: '#app-qualify-btn',
    backBtn: '#app-back-btn',

    // Botones de selección de Plataforma
    platformWeb: '.platform-btn[data-platform="web"]',
    platformMobile: '.platform-btn[data-platform="mobile"]',
    platformMulti: '.platform-btn[data-platform="multi"]',

    // Botones de selección de Integración
    integrationBase: '.integration-btn[data-integration="base"]',
    integrationIa: '.integration-btn[data-integration="ia"]',
    integrationEnterprise: '.integration-btn[data-integration="enterprise"]',

    // Controles adicionales
    usersSlider: '#app-users',
    usersVal: '#app-users-val',
    industrySelect: '#app-industry',

    // Pantallas de CTAs y enlaces resultantes
    ctaLowCost: '#cta-low-cost',
    ctaHighCost: '#cta-high-cost',
    whatsappCtaLink: '#whatsapp-cta-link',
    calCtaButton: 'button[data-cal-link="localexpert/consultorialocalexpert"]',
    
    // Resultados en tiempo real
    costVal: '#app-cost-val',
    revenueVal: '#app-revenue-val',
    roiVal: '#app-roi-val',
    timeVal: '#app-time-val'
};

// Determinar la URL objetivo (prioriza servidor de desarrollo local, si no, usa file://)
function getTargetUrl() {
    const baseUrl = process.env.TEST_BASE_URL || 'http://localhost:3000';
    return `${baseUrl}/desarrollo-apps-software/colombia/bogota/index.html`;
}

// Helper para extraer la tasa de conversión a partir del texto del costo
function getConversionRate(costText) {
    const text = costText.trim().toUpperCase();
    if (text.includes('COP')) {
        return 4000;
    } else if (text.includes('MXN')) {
        return 18;
    } else if (text.includes('ARS')) {
        return 1000;
    } else {
        // Por defecto asumimos USD
        return 1;
    }
}

test.describe('Consultor IA - Landing Pages QA & SEO & Simulador de Costo', () => {
    let targetUrl;
    let consoleErrors = [];
    let pageErrors = [];

    test.beforeAll(() => {
        targetUrl = getTargetUrl();
        console.log(`[QA SETUP] URL de pruebas objetivo: ${targetUrl}`);
    });

    test.beforeEach(({ page }) => {
        consoleErrors = [];
        pageErrors = [];

        // Capturar errores de consola
        page.on('console', msg => {
            if (msg.type() === 'error') {
                consoleErrors.push(`[Console Error] ${msg.text()}`);
                console.log(`🔴 Consola Error: ${msg.text()}`);
            }
        });

        // Capturar errores no controlados de JavaScript
        page.on('pageerror', err => {
            pageErrors.push(`[Page Error] ${err.message}`);
            console.log(`🔴 JS Error: ${err.message}`);
        });
    });

    test.afterEach(async () => {
        if (consoleErrors.length > 0) {
            console.log(`⚠️ Se detectaron ${consoleErrors.length} errores de consola durante la ejecución.`);
        }
        if (pageErrors.length > 0) {
            console.log(`⚠️ Se detectaron ${pageErrors.length} errores de JavaScript no controlados.`);
        }
    });

    test('1. Auditoría SEO - Títulos, Meta Descriptions y H1 único', async ({ page }) => {
        console.log(`[SEO Test] Navegando a: ${targetUrl}`);
        const response = await page.goto(targetUrl);
        expect(response.status()).toBe(200);
        await page.waitForLoadState('domcontentloaded');

        // A. Verificar etiqueta title
        const title = await page.title();
        console.log(`SEO Title detectado: "${title}"`);
        expect(title).toBeTruthy();
        expect(title.length).toBeGreaterThan(10);
        expect(title).not.toContain('{');
        expect(title).not.toContain('}');

        // B. Verificar meta description
        const descriptionMeta = page.locator('meta[name="description"]');
        await expect(descriptionMeta).toHaveCount(1);
        
        const descriptionContent = await descriptionMeta.getAttribute('content');
        console.log(`SEO Description detectada: "${descriptionContent}"`);
        expect(descriptionContent).toBeTruthy();
        expect(descriptionContent.length).toBeGreaterThan(30);
        expect(descriptionContent).not.toContain('{');
        expect(descriptionContent).not.toContain('}');

        // C. Estructura H1 única
        const h1Elements = page.locator('h1');
        const h1Count = await h1Elements.count();
        console.log(`Estructura H1: Se encontraron ${h1Count} elemento(s) H1.`);
        expect(h1Count).toBe(1);

        const h1Text = await h1Elements.first().innerText();
        console.log(`H1 Contenido: "${h1Text.trim()}"`);
        expect(h1Text.trim()).not.toBe('');
        expect(h1Text).not.toContain('{');
        expect(h1Text).not.toContain('}');
    });

    test('2. Simulador de Costo y ROI - Selección de Bajo Presupuesto (WhatsApp/No-code)', async ({ page }) => {
        console.log(`[Bajo Presupuesto Test] Navegando a: ${targetUrl}`);
        await page.goto(targetUrl);
        await page.waitForLoadState('domcontentloaded');

        // Verificar presencia del simulador y de los botones iniciales
        const qualifyBtn = page.locator(SELECTORS.qualifyBtn);
        await expect(qualifyBtn).toBeVisible();

        console.log('🟢 Simulador de Costo y ROI de App detectado y listo para interacción.');

        // Configurar Bajo Presupuesto (< 5000 USD):
        // 1. Plataforma: Web App (Costo: 2500)
        console.log('Seleccionando Plataforma: Web App / PWA');
        await page.locator(SELECTORS.platformWeb).click();

        // 2. Integración: Base (Costo: 1000)
        console.log('Seleccionando Integración: Base (Sin IA compleja)');
        await page.locator(SELECTORS.integrationBase).click();

        // 3. Usuarios Proyectados: Mínimo valor en slider (1000) para evitar costo por escala
        console.log('Ajustando usuarios proyectados al mínimo (1,000 / mes)');
        const slider = page.locator(SELECTORS.usersSlider);
        await slider.fill('1000');
        await slider.dispatchEvent('input');

        // 4. Sector: Servicios (factor 1.0)
        console.log('Seleccionando Sector: Servicios');
        await page.locator(SELECTORS.industrySelect).selectOption('servicios');

        // Esperar cálculo en UI y verificar costo estimado en pantalla
        await page.waitForTimeout(300);
        const costText = await page.locator(SELECTORS.costVal).innerText();
        console.log(`Costo estimado en pantalla: ${costText}`);
        
        // Obtener la tasa de conversión basada en la moneda detectada
        const rate = getConversionRate(costText);
        console.log(`Moneda detectada. Tasa de conversión aplicada: ${rate}`);

        // Convertir el costo en pantalla a número
        const costNumeric = parseInt(costText.replace(/[^0-9]/g, ''));
        console.log(`Costo numérico limpio: ${costNumeric}`);
        
        // Calcular el umbral en moneda local (5000 USD * rate)
        const umbralLocal = 5000 * rate;
        console.log(`Umbral en moneda local para comparación: ${umbralLocal}`);

        // El costo debe ser estrictamente menor al umbral en moneda local
        expect(costNumeric).toBeLessThan(umbralLocal);

        // Hacer clic en "Ver Recomendación y Siguiente Paso"
        console.log('Haciendo clic en "Ver Recomendación" para calificar...');
        await qualifyBtn.click();

        // Verificar transición de pantalla
        await expect(page.locator(SELECTORS.ctaScreen)).toBeVisible();
        await expect(page.locator(SELECTORS.resultsScreen)).toBeHidden();

        // Verificar que se muestre el CTA de WhatsApp (Bajo Costo) y se oculte el de Calendly (Alto Costo)
        console.log('Validando que se visualice la recomendación de MVP No-Code / Chatbot...');
        await expect(page.locator(SELECTORS.ctaLowCost)).toBeVisible();
        await expect(page.locator(SELECTORS.ctaHighCost)).toBeHidden();

        // Verificar el enlace de redirección a WhatsApp
        const whatsappLink = page.locator(SELECTORS.whatsappCtaLink);
        const href = await whatsappLink.getAttribute('href');
        console.log(`Enlace de WhatsApp generado: ${href}`);
        expect(href).toMatch(/wa\.me/i);
        expect(href).toContain(encodeURIComponent('MVP No-Code / Chatbot'));
    });

    test('3. Simulador de Costo y ROI - Selección de Alto Presupuesto (Booking CTA)', async ({ page }) => {
        console.log(`[Alto Presupuesto Test] Navegando a: ${targetUrl}`);
        await page.goto(targetUrl);
        await page.waitForLoadState('domcontentloaded');

        // Verificar presencia del simulador
        const qualifyBtn = page.locator(SELECTORS.qualifyBtn);
        await expect(qualifyBtn).toBeVisible();

        // Configurar Alto Presupuesto (>= 5000 USD):
        // 1. Plataforma: Multiplataforma (Costo: 9500)
        console.log('Seleccionando Plataforma: Multiplataforma');
        await page.locator(SELECTORS.platformMulti).click();

        // 2. Integración: Enterprise (Costo: 6000)
        console.log('Seleccionando Integración: ERP & Avanzado');
        await page.locator(SELECTORS.integrationEnterprise).click();

        // Esperar cálculo en UI y verificar costo estimado en pantalla
        await page.waitForTimeout(300);
        const costText = await page.locator(SELECTORS.costVal).innerText();
        console.log(`Costo estimado en pantalla: ${costText}`);
        
        // Obtener la tasa de conversión basada en la moneda detectada
        const rate = getConversionRate(costText);
        console.log(`Moneda detectada. Tasa de conversión aplicada: ${rate}`);

        // Convertir el costo en pantalla a número
        const costNumeric = parseInt(costText.replace(/[^0-9]/g, ''));
        console.log(`Costo numérico limpio: ${costNumeric}`);
        
        // Calcular el umbral en moneda local (5000 USD * rate)
        const umbralLocal = 5000 * rate;
        console.log(`Umbral en moneda local para comparación: ${umbralLocal}`);

        // El costo debe superar o ser igual al umbral en moneda local
        expect(costNumeric).toBeGreaterThanOrEqual(umbralLocal);

        // Hacer clic en "Ver Recomendación y Siguiente Paso"
        console.log('Haciendo clic en "Ver Recomendación" para calificar...');
        await qualifyBtn.click();

        // Verificar transición de pantalla
        await expect(page.locator(SELECTORS.ctaScreen)).toBeVisible();

        // Verificar que se muestre el CTA de Calendly (Alto Costo) y se oculte el de WhatsApp
        console.log('Validando que se visualice la recomendación de Consultoría IA-Native...');
        await expect(page.locator(SELECTORS.ctaHighCost)).toBeVisible();
        await expect(page.locator(SELECTORS.ctaLowCost)).toBeHidden();

        // Verificar que el botón de Cal con atributos correctos esté presente
        const calButton = page.locator(SELECTORS.ctaHighCost).locator(SELECTORS.calCtaButton);
        await expect(calButton).toBeVisible();
        const calLinkAttr = await calButton.getAttribute('data-cal-link');
        const calNamespaceAttr = await calButton.getAttribute('data-cal-namespace');
        console.log(`Botón de Cal detectado. Link: ${calLinkAttr}, Namespace: ${calNamespaceAttr}`);
        expect(calLinkAttr).toBe('localexpert/consultorialocalexpert');
        expect(calNamespaceAttr).toBe('consultorialocalexpert');
    });

    test('4. Detección de Errores Críticos de Carga (Sin errores de consola/JS)', async ({ page }) => {
        console.log(`[Detección Errores Test] Navegando a: ${targetUrl}`);
        await page.goto(targetUrl);
        await page.waitForLoadState('networkidle');

        // Validar que no haya excepciones o errores JavaScript fatales
        expect(pageErrors.length).toBe(0);

        // Validar que no haya recursos fallidos de red importantes en la consola (como CSS, JS que causan net::ERR_FILE_NOT_FOUND)
        const criticalConsoleErrors = consoleErrors.filter(err => !err.includes('favicon.ico'));
        expect(criticalConsoleErrors.length).toBe(0);
    });
});
