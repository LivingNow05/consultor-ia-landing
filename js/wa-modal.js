(function () {
  // ─── Inyección de estilos dedicados y estructura del modal B2B (2 pasos) ───
  const modalStyles = `
  <style id="wa-modal-inline-styles">
    #wa-modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      width: 100vw;
      height: 100vh;
      z-index: 999999;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 16px;
      box-sizing: border-box;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.22s ease;
    }
    #wa-modal-overlay.wa-open {
      opacity: 1;
      pointer-events: auto;
    }
    #wa-modal-backdrop {
      position: absolute;
      inset: 0;
      background: rgba(0, 0, 0, 0.72);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      z-index: 1;
    }
    #wa-modal-card {
      position: relative;
      z-index: 2;
      width: 100%;
      max-width: 540px;
      margin: auto;
      border-radius: 24px;
      padding: 30px 26px 22px;
      box-sizing: border-box;
      background: #ffffff;
      color: #18181b;
      border: 1px solid #e4e4e7;
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(0,0,0,0.05);
      transform: scale(0.96);
      transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.22s ease;
    }
    .dark #wa-modal-card {
      background: #09090b;
      color: #f4f4f5;
      border-color: #27272a;
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255,255,255,0.08);
    }
    #wa-modal-overlay.wa-open #wa-modal-card {
      transform: scale(1);
    }
    #wa-modal-close {
      position: absolute;
      top: 16px;
      right: 16px;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid rgba(0, 0, 0, 0.08);
      background: rgba(0, 0, 0, 0.04);
      color: #71717a;
      font-size: 15px;
      cursor: pointer;
      transition: all 0.2s ease;
      outline: none;
      padding: 0;
    }
    #wa-modal-close:hover {
      background: rgba(0, 0, 0, 0.08);
      color: #18181b;
      transform: scale(1.06);
    }
    .dark #wa-modal-close {
      border-color: rgba(255, 255, 255, 0.1);
      background: rgba(255, 255, 255, 0.06);
      color: #a1a1aa;
    }
    .dark #wa-modal-close:hover {
      background: rgba(255, 255, 255, 0.15);
      color: #ffffff;
    }
    .wa-options-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }
    .wa-options-grid.wa-cols-3 {
      grid-template-columns: 1fr;
    }
    @media (max-width: 520px) {
      .wa-options-grid {
        grid-template-columns: 1fr;
      }
      #wa-modal-card {
        padding: 24px 18px 18px;
      }
    }
    .wa-modal-opt {
      background: #fdfbf7;
      border: 1px solid #e4e4e7;
      border-radius: 16px;
      padding: 15px 16px;
      text-align: left;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 14px;
      transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
      outline: none;
      user-select: none;
      width: 100%;
    }
    .wa-modal-opt:hover {
      background: #ffffff;
      border-color: #2563eb;
      transform: translateY(-2px);
      box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.12);
    }
    .dark .wa-modal-opt {
      background: #18181b;
      border-color: #27272a;
      color: #f4f4f5;
    }
    .dark .wa-modal-opt:hover {
      background: #27272a;
      border-color: #3b82f6;
      box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.5);
    }
    .wa-opt-icon-wrap {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      background: rgba(37, 99, 235, 0.08);
      color: #2563eb;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      font-size: 18px;
      transition: all 0.2s ease;
    }
    .wa-modal-opt:hover .wa-opt-icon-wrap {
      background: #2563eb;
      color: #ffffff;
    }
    .dark .wa-opt-icon-wrap {
      background: rgba(59, 130, 246, 0.15);
      color: #60a5fa;
    }
    .dark .wa-modal-opt:hover .wa-opt-icon-wrap {
      background: #3b82f6;
      color: #ffffff;
    }
    .wa-opt-text {
      display: flex;
      flex-direction: column;
      min-width: 0;
    }
    .wa-opt-label {
      font-size: 14px;
      font-weight: 700;
      color: #18181b;
      margin-bottom: 2px;
      line-height: 1.25;
    }
    .dark .wa-opt-label {
      color: #f4f4f5;
    }
    .wa-opt-sub {
      font-size: 12px;
      color: #71717a;
      line-height: 1.35;
    }
    .dark .wa-opt-sub {
      color: #a1a1aa;
    }
    .wa-skip-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      margin-top: 16px;
      font-size: 12px;
      font-weight: 600;
      color: #71717a;
      text-decoration: none;
      cursor: pointer;
      background: transparent;
      border: none;
      padding: 6px 12px;
      border-radius: 9999px;
      transition: all 0.2s ease;
    }
    .wa-skip-btn:hover {
      color: #18181b;
      background: rgba(0,0,0,0.04);
    }
    .dark .wa-skip-btn {
      color: #a1a1aa;
    }
    .dark .wa-skip-btn:hover {
      color: #f4f4f5;
      background: rgba(255,255,255,0.06);
    }
  </style>
  `;

  const modalHTML = `
  ${modalStyles}
  <div id="wa-modal-overlay" class="wa-modal-hidden" role="dialog" aria-modal="true" aria-labelledby="wa-modal-title">
    <div id="wa-modal-backdrop"></div>
    <div id="wa-modal-card">

      <!-- Botón de Cerrar -->
      <button id="wa-modal-close" aria-label="Cerrar modal">
        <i class="fas fa-times"></i>
      </button>

      <!-- Intro -->
      <div style="text-align: center; margin-bottom: 14px;">
        <span style="font-size: 10px; font-weight: 800; letter-spacing: 0.16em; text-transform: uppercase; color: #2563eb; display: block; margin-bottom: 5px;">
          Atención B2B Inmediata • Paso <span id="wa-step-counter">1</span> de 2
        </span>
        <h2 id="wa-modal-title" style="font-size: 20px; font-weight: 800; margin: 0 0 4px 0; line-height: 1.25;">
          Conectemos con un ingeniero especialista
        </h2>
        <p style="font-size: 12px; color: #71717a; margin: 0; line-height: 1.4;">
          Selecciona 2 opciones rápidas para preparar tu cotización en WhatsApp.
        </p>
      </div>

      <!-- Barra de progreso -->
      <div id="wa-modal-progress" style="display: flex; gap: 6px; margin: 14px 0 18px 0;"></div>

      <!-- Steps container -->
      <div id="wa-modal-steps" style="transition: opacity 0.18s ease; opacity: 1;"></div>

      <!-- Enlace para omitir e ir directo a WhatsApp -->
      <div style="text-align: center;">
        <button id="wa-modal-skip" class="wa-skip-btn" type="button">
          <span>Ir directo a WhatsApp sin responder</span>
          <i class="fas fa-arrow-right" style="font-size: 10px;"></i>
        </button>
      </div>

    </div>
  </div>`;

  document.body.insertAdjacentHTML('beforeend', modalHTML);

  // ─── Estado ─────────────────────────────────────────────────────────────────
  const SESSION_KEY = 'consultoria_wa_profile_v2';
  const state = { solution: '', intent: '' };
  let currentStep = 0;
  let pendingHref = '';
  let isAnimating = false;

  // Definición de 2 pasos de alta conversión B2B
  const steps = [
    {
      key: 'solution',
      cols: 3,
      question: '1. ¿Qué solución buscas implementar en tu empresa?',
      options: [
        { value: 'agente_whatsapp', icon: 'fa-robot',          label: 'Agente IA para WhatsApp',       sub: 'Atención 24/7, calificación de leads y agendamiento ($497 Setup + $97/mes)' },
        { value: 'flujos_crm',      icon: 'fa-diagram-project',label: 'Flujos Inteligentes y CRM',     sub: 'Automatización de procesos comerciales, HubSpot, Kommo o ERP' },
        { value: 'medida_b2b',      icon: 'fa-microchip',      label: 'Ecosistema IA a Medida (B2B)',  sub: 'Arquitectura multi-agente, reglas de negocio complejas y APIs' }
      ]
    },
    {
      key: 'intent',
      cols: 2,
      question: '2. ¿Cómo prefieres avanzar con nuestro equipo?',
      options: [
        { value: 'cotizacion',  icon: 'fa-file-invoice-dollar', label: 'Solicitar Cotización',     sub: 'Recibir propuesta económica y alcance hoy' },
        { value: 'diagnostico', icon: 'fa-calendar-check',      label: 'Diagnóstico de 15 min',    sub: 'Revisar mi flujo actual con un consultor' }
      ]
    }
  ];

  const totalSteps = steps.length;

  function trackModalEvent(eventName, params) {
    if (window.ConsultorAnalytics && typeof window.ConsultorAnalytics.track === 'function') {
      window.ConsultorAnalytics.track(eventName, params || {});
    } else {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(Object.assign({ event: eventName }, params || {}));
    }
  }

  // ─── Helpers ────────────────────────────────────────────────────────────────
  function buildProgressBar() {
    const bar = document.getElementById('wa-modal-progress');
    const counter = document.getElementById('wa-step-counter');
    if (counter) counter.textContent = String(currentStep + 1);
    if (!bar) return;
    bar.innerHTML = '';
    for (let i = 0; i < totalSteps; i++) {
      const seg = document.createElement('div');
      seg.style.height = '5px';
      seg.style.borderRadius = '9999px';
      seg.style.flex = '1';
      seg.style.transition = 'background-color 0.25s ease';
      seg.style.backgroundColor = (i <= currentStep) ? '#2563eb' : 'rgba(113, 113, 122, 0.2)';
      bar.appendChild(seg);
    }
  }

  function buildStepHTML(step) {
    const gridClass = step.cols === 3 ? 'wa-options-grid wa-cols-3' : 'wa-options-grid';
    return `
      <h3 style="font-size: 15px; font-weight: 700; text-align: center; margin: 0 0 14px 0;">
        ${step.question}
      </h3>
      <div class="${gridClass}">
        ${step.options.map(opt => `
          <button type="button" class="wa-modal-opt" data-key="${step.key}" data-val="${opt.value}">
            <div class="wa-opt-icon-wrap">
              <i class="fas ${opt.icon}"></i>
            </div>
            <div class="wa-opt-text">
              <span class="wa-opt-label">${opt.label}</span>
              <span class="wa-opt-sub">${opt.sub}</span>
            </div>
          </button>`).join('')}
      </div>`;
  }

  function attachStepListeners() {
    const container = document.getElementById('wa-modal-steps');
    if (!container) return;
    container.querySelectorAll('.wa-modal-opt').forEach(btn => {
      btn.addEventListener('click', function () {
        if (isAnimating) return;
        const key = this.dataset.key;
        const val = this.dataset.val;
        state[key] = val;

        trackModalEvent('wa_modal_step', {
          step_number: currentStep + 1,
          step_key: key,
          step_value: val
        });

        currentStep++;
        if (currentStep < steps.length) {
          goToStep();
        } else {
          try {
            sessionStorage.setItem(SESSION_KEY, JSON.stringify(state));
          } catch (e) {}
          finalize(false);
        }
      });
    });
  }

  function goToStep() {
    if (isAnimating) return;
    isAnimating = true;

    const container = document.getElementById('wa-modal-steps');
    if (!container) return;
    container.style.opacity = '0';

    setTimeout(function () {
      buildProgressBar();
      container.innerHTML = buildStepHTML(steps[currentStep]);
      attachStepListeners();
      void container.offsetHeight;
      container.style.opacity = '1';
      isAnimating = false;
    }, 170);
  }

  function renderStep() {
    buildProgressBar();
    const container = document.getElementById('wa-modal-steps');
    if (!container) return;
    container.style.opacity = '1';
    container.innerHTML = buildStepHTML(steps[currentStep]);
    attachStepListeners();
  }

  // ─── Construcción del mensaje con datos parciales o completos ──────────────
  function buildMessage(profileData) {
    const data = profileData || state;
    const labels = {
      solution: {
        agente_whatsapp: 'Agente IA para WhatsApp ($497 Setup + $97/mes)',
        flujos_crm: 'Flujos Inteligentes y Conexión CRM',
        medida_b2b: 'Ecosistema IA a Medida (B2B)'
      },
      intent: {
        cotizacion: 'Solicitar Cotización Comercial',
        diagnostico: 'Agendar Diagnóstico Técnico (15 min)'
      }
    };

    const lines = [];
    if (data.solution && labels.solution[data.solution]) {
      lines.push(`▪ Solución de interés: ${labels.solution[data.solution]}`);
    }
    if (data.intent && labels.intent[data.intent]) {
      lines.push(`▪ Siguiente paso: ${labels.intent[data.intent]}`);
    }

    if (lines.length === 0) return '';
    return `\n\n[ Solicitud B2B ]\n` + lines.join('\n');
  }

  function appendMessageToHref(href, extraMessage) {
    if (!extraMessage) return href;
    try {
      const urlObj = new URL(href);
      let currentText = urlObj.searchParams.get('text') || '';
      if (!currentText.trim()) {
        currentText = 'Hola, quiero información sobre automatización con IA para mi empresa.';
      }
      urlObj.searchParams.set('text', currentText + extraMessage);
      return urlObj.toString();
    } catch (e) {
      if (href.includes('?text=')) {
        return href + encodeURIComponent(extraMessage);
      }
      return href + '?text=' + encodeURIComponent(extraMessage);
    }
  }

  function finalize(wasSkipped, customProfile) {
    const profileToUse = customProfile || state;
    const extraMsg = buildMessage(profileToUse);
    const finalUrl = appendMessageToHref(pendingHref, extraMsg);

    trackModalEvent('wa_lead_redirect', {
      solution: profileToUse.solution || 'unspecified',
      intent: profileToUse.intent || 'unspecified',
      skipped: !!wasSkipped,
      destination_url: finalUrl
    });

    closeModal();
    window.open(finalUrl, '_blank', 'noopener,noreferrer');
  }

  // ─── Control del modal ───────────────────────────────────────────────────────
  function openModal(originalHref) {
    pendingHref = originalHref;

    // Si el usuario ya completó el perfil en esta sesión, no volver a mostrar el modal
    try {
      const savedProfileRaw = sessionStorage.getItem(SESSION_KEY);
      if (savedProfileRaw) {
        const savedProfile = JSON.parse(savedProfileRaw);
        if (savedProfile && savedProfile.solution) {
          finalize(false, savedProfile);
          return;
        }
      }
    } catch (e) {}

    currentStep = 0;
    isAnimating = false;
    Object.keys(state).forEach(k => state[k] = '');

    renderStep();
    const overlay = document.getElementById('wa-modal-overlay');
    if (!overlay) return;

    overlay.classList.add('wa-open');
    document.body.style.overflow = 'hidden';

    trackModalEvent('wa_modal_open', {
      trigger_href: originalHref
    });
  }

  function closeModal() {
    const overlay = document.getElementById('wa-modal-overlay');
    if (!overlay) return;

    overlay.classList.remove('wa-open');
    document.body.style.overflow = '';
  }

  const closeBtn = document.getElementById('wa-modal-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      closeModal();
    });
  }

  const backdrop = document.getElementById('wa-modal-backdrop');
  if (backdrop) {
    backdrop.addEventListener('click', function (e) {
      e.stopPropagation();
      closeModal();
    });
  }

  // Botón para saltar e ir a WhatsApp conservando respuestas parciales si las hay
  const skipBtn = document.getElementById('wa-modal-skip');
  if (skipBtn) {
    skipBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      trackModalEvent('wa_modal_skip', {
        step_abandoned: currentStep + 1,
        partial_solution: state.solution || 'none'
      });
      finalize(true);
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      const overlay = document.getElementById('wa-modal-overlay');
      if (overlay && overlay.classList.contains('wa-open')) {
        closeModal();
      }
    }
  });

  // ─── Interceptar todos los botones WhatsApp ──────────────────────────────────
  document.addEventListener('click', function (e) {
    const link = e.target.closest('a[href*="wa.me"], a[href*="api.whatsapp.com"]');
    if (!link) return;

    if (link.dataset.noModal === 'true') return;

    e.preventDefault();
    openModal(link.href);
  });

})();
