(function () {
  // ─── Inyección de estilos dedicados y estructura del modal ──────────────────
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
      transition: opacity 0.25s ease;
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
      max-width: 530px;
      margin: auto;
      border-radius: 24px;
      padding: 32px 28px 24px;
      box-sizing: border-box;
      background: #ffffff;
      color: #18181b;
      border: 1px solid #e4e4e7;
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(0,0,0,0.05);
      transform: scale(0.95);
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
    }
    .dark #wa-modal-card {
      background: #09090b;
      color: #f4f4f5;
      border-color: #27272a;
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(255,255,255,0.08);
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
      font-size: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
      outline: none;
      padding: 0;
    }
    #wa-modal-close:hover {
      background: rgba(0, 0, 0, 0.08);
      color: #18181b;
      transform: scale(1.08);
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
      gap: 12px;
    }
    @media (max-width: 520px) {
      .wa-options-grid {
        grid-template-columns: 1fr;
      }
      #wa-modal-card {
        padding: 26px 18px 20px;
      }
    }
    .wa-modal-opt {
      background: #fdfbf7;
      border: 1px solid #e4e4e7;
      border-radius: 18px;
      padding: 18px 14px;
      text-align: center;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      outline: none;
      user-select: none;
    }
    .wa-modal-opt:hover {
      background: #ffffff;
      border-color: #18181b;
      transform: translateY(-2px);
      box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.08);
    }
    .dark .wa-modal-opt {
      background: #18181b;
      border-color: #27272a;
      color: #f4f4f5;
    }
    .dark .wa-modal-opt:hover {
      background: #27272a;
      border-color: #f4f4f5;
      box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.5);
    }
    .wa-opt-icon {
      font-size: 26px;
      color: #71717a;
      margin-bottom: 10px;
      transition: color 0.2s ease, transform 0.2s ease;
    }
    .wa-modal-opt:hover .wa-opt-icon {
      color: #18181b;
      transform: scale(1.1);
    }
    .dark .wa-opt-icon {
      color: #a1a1aa;
    }
    .dark .wa-modal-opt:hover .wa-opt-icon {
      color: #ffffff;
    }
    .wa-opt-label {
      font-size: 15px;
      font-weight: 700;
      color: #18181b;
      margin-bottom: 4px;
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
      margin-top: 18px;
      font-size: 13px;
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

      <!-- Botón de Cerrar (limpio, sin abrir WhatsApp) -->
      <button id="wa-modal-close" aria-label="Cerrar modal">
        <i class="fas fa-times"></i>
      </button>

      <!-- Intro -->
      <div style="text-align: center; margin-bottom: 16px;">
        <span style="font-size: 11px; font-weight: 800; letter-spacing: 0.15em; text-transform: uppercase; color: #2563eb; display: block; margin-bottom: 6px;">
          Personalización de Asesoría
        </span>
        <h2 id="wa-modal-title" style="font-size: 22px; font-weight: 800; margin: 0 0 6px 0; line-height: 1.25;">
          Cuéntanos sobre tu empresa
        </h2>
        <p style="font-size: 13px; color: #71717a; margin: 0; line-height: 1.4;">
          Para asignarte al consultor experto ideal para tu caso.
        </p>
      </div>

      <!-- Barra de progreso -->
      <div id="wa-modal-progress" style="display: flex; gap: 6px; margin: 18px 0 22px 0;"></div>

      <!-- Steps container -->
      <div id="wa-modal-steps" style="transition: opacity 0.25s ease; opacity: 1;"></div>

      <!-- Enlace para omitir e ir directo a WhatsApp -->
      <div style="text-align: center;">
        <button id="wa-modal-skip" class="wa-skip-btn" type="button">
          <span>Omitir preguntas y chatear directo en WhatsApp</span>
          <i class="fas fa-arrow-right" style="font-size: 11px;"></i>
        </button>
      </div>

    </div>
  </div>`;

  document.body.insertAdjacentHTML('beforeend', modalHTML);

  // ─── Estado ─────────────────────────────────────────────────────────────────
  const state = { size: '', goal: '', crm: '', urgency: '' };
  let currentStep = 0;
  let pendingHref = '';
  let isAnimating = false;

  // Definición de pasos
  const steps = [
    {
      key: 'size',
      question: '¿De qué tamaño es tu empresa?',
      options: [
        { value: 'pequena', icon: 'fa-store',     label: 'Pequeña',           sub: 'De 1 a 10 empleados' },
        { value: 'mediana', icon: 'fa-building',  label: 'Mediana / Grande',  sub: 'Más de 10 empleados' }
      ]
    },
    {
      key: 'goal',
      question: '¿Qué área buscas automatizar con IA?',
      options: [
        { value: 'ventas',      icon: 'fa-comments',  label: 'Ventas y Atención',  sub: 'Chatbots, WhatsApp, CRM' },
        { value: 'operaciones', icon: 'fa-gears',     label: 'Operaciones',        sub: 'Procesos internos y Datos' }
      ]
    },
    {
      key: 'crm',
      question: '¿Cómo gestionan a sus clientes hoy?',
      options: [
        { value: 'crm',   icon: 'fa-laptop-code',  label: 'Usamos un CRM',   sub: 'HubSpot, Kommo, etc.' },
        { value: 'excel', icon: 'fa-file-excel',   label: 'Excel / Manual',  sub: 'Planillas o chat manual' }
      ]
    },
    {
      key: 'urgency',
      question: '¿Cuál es tu nivel de urgencia?',
      options: [
        { value: 'pronto',     icon: 'fa-bolt',     label: 'Lo necesito pronto',  sub: 'Implementar este mes' },
        { value: 'explorando', icon: 'fa-compass',  label: 'Estoy explorando',    sub: 'Evaluando opciones' }
      ]
    }
  ];

  const totalSteps = steps.length;

  // ─── Helpers ────────────────────────────────────────────────────────────────
  function buildProgressBar() {
    const bar = document.getElementById('wa-modal-progress');
    if (!bar) return;
    bar.innerHTML = '';
    for (let i = 0; i < totalSteps; i++) {
      const seg = document.createElement('div');
      seg.style.height = '5px';
      seg.style.borderRadius = '9999px';
      seg.style.flex = '1';
      seg.style.transition = 'background-color 0.3s ease';
      seg.style.backgroundColor = (i <= currentStep) ? '#2563eb' : 'rgba(113, 113, 122, 0.2)';
      bar.appendChild(seg);
    }
  }

  function buildStepHTML(step) {
    return `
      <h3 style="font-size: 16px; font-weight: 700; text-align: center; margin: 0 0 16px 0;">
        ${step.question}
      </h3>
      <div class="wa-options-grid">
        ${step.options.map(opt => `
          <button type="button" class="wa-modal-opt" data-key="${step.key}" data-val="${opt.value}">
            <i class="fas ${opt.icon} wa-opt-icon"></i>
            <span class="wa-opt-label">${opt.label}</span>
            <span class="wa-opt-sub">${opt.sub}</span>
          </button>`).join('')}
      </div>`;
  }

  function attachStepListeners(step) {
    const container = document.getElementById('wa-modal-steps');
    if (!container) return;
    container.querySelectorAll('.wa-modal-opt').forEach(btn => {
      btn.addEventListener('click', function () {
        if (isAnimating) return;
        state[this.dataset.key] = this.dataset.val;
        currentStep++;
        if (currentStep < steps.length) {
          goToStep();
        } else {
          finalize();
        }
      });
    });
  }

  // ─── Animación de cambio de paso ─────────────────────────────────────────────
  function goToStep() {
    if (isAnimating) return;
    isAnimating = true;

    const container = document.getElementById('wa-modal-steps');
    if (!container) return;
    container.style.opacity = '0';

    setTimeout(function () {
      buildProgressBar();
      container.innerHTML = buildStepHTML(steps[currentStep]);
      attachStepListeners(steps[currentStep]);
      void container.offsetHeight; // trigger reflow
      container.style.opacity = '1';
      isAnimating = false;
    }, 220);
  }

  function renderStep() {
    buildProgressBar();
    const container = document.getElementById('wa-modal-steps');
    if (!container) return;
    container.style.opacity = '1';
    container.innerHTML = buildStepHTML(steps[currentStep]);
    attachStepListeners(steps[currentStep]);
  }

  // ─── Construcción del mensaje ────────────────────────────────────────────────
  function buildMessage() {
    const labels = {
      size:    { pequena: 'Pequeña (1-10 emp.)', mediana: 'Mediana/Grande (+10 emp.)' },
      goal:    { ventas: 'Ventas y Atención', operaciones: 'Operaciones e Interno' },
      crm:     { crm: 'Sí, usamos un CRM', excel: 'No, usamos Excel / Manual' },
      urgency: { pronto: 'Alta (Quiero implementar pronto)', explorando: 'Baja (Solo explorando opciones)' }
    };

    let msg = `\n\n[ Perfil de Empresa ]\n`;
    msg += `▪ Tamaño: ${labels.size[state.size] || state.size}\n`;
    msg += `▪ Objetivo principal: ${labels.goal[state.goal] || state.goal}\n`;
    msg += `▪ Gestión actual: ${labels.crm[state.crm] || state.crm}\n`;
    msg += `▪ Urgencia: ${labels.urgency[state.urgency] || state.urgency}`;
    return msg;
  }

  function finalize() {
    let finalUrl = pendingHref;
    
    try {
      const urlObj = new URL(pendingHref);
      let currentText = urlObj.searchParams.get('text') || '';
      
      if (!currentText.trim()) {
        currentText = "Hola, me interesa agendar una asesoría sobre automatización con IA.";
      }
      
      const msg = buildMessage();
      urlObj.searchParams.set('text', currentText + msg);
      finalUrl = urlObj.toString();
    } catch (e) {
      if (pendingHref.includes('?text=')) {
        finalUrl = pendingHref + encodeURIComponent(buildMessage());
      } else {
        finalUrl = pendingHref + '?text=' + encodeURIComponent(buildMessage());
      }
    }

    closeModal();
    window.open(finalUrl, '_blank');
  }

  // ─── Control del modal ───────────────────────────────────────────────────────
  function openModal(originalHref) {
    pendingHref = originalHref;
    currentStep = 0;
    isAnimating = false;
    
    // Limpiar estado
    Object.keys(state).forEach(k => state[k] = '');
    
    renderStep();
    const overlay = document.getElementById('wa-modal-overlay');
    if (!overlay) return;
    
    overlay.classList.add('wa-open');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    const overlay = document.getElementById('wa-modal-overlay');
    if (!overlay) return;
    
    overlay.classList.remove('wa-open');
    document.body.style.overflow = '';
  }

  // Cerrar limpiamente con × o backdrop (SIN forzar abrir WhatsApp)
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

  // Botón para saltar e ir a WhatsApp voluntariamente
  const skipBtn = document.getElementById('wa-modal-skip');
  if (skipBtn) {
    skipBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      closeModal();
      if (pendingHref) window.open(pendingHref, '_blank');
    });
  }

  // Cerrar con tecla Escape
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
    
    // Excluir si ya tiene un flujo especial o no queremos modal
    if (link.dataset.noModal === 'true') return;

    e.preventDefault();
    openModal(link.href);
  });

})();
