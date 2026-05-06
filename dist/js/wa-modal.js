(function () {
  // ─── Inyección del modal en el DOM ──────────────────────────────────────────
  const modalHTML = `
  <div id="wa-modal-overlay" style="display:none" class="fixed inset-0 z-[9999] flex items-center justify-center p-4 font-sans" role="dialog" aria-modal="true">
    <div class="absolute inset-0 bg-black/60 backdrop-blur-md" id="wa-modal-backdrop"></div>
    <div class="relative bg-[#FDFBF7] dark:bg-zinc-950 rounded-3xl shadow-2xl border border-gray-border dark:border-zinc-800 w-full max-w-lg p-8 z-10 transition-all scale-95 opacity-0 duration-300" id="wa-modal-card">

      <!-- Cerrar -->
      <button id="wa-modal-close" class="absolute top-4 right-5 text-gray-2 dark:text-slate-400 hover:text-brand dark:hover:text-brand-light text-2xl font-bold leading-none transition-colors" aria-label="Cerrar">&times;</button>

      <!-- Intro -->
      <div class="text-center mb-4">
        <span class="text-brand dark:text-brand-light font-bold text-xs tracking-widest uppercase mb-2 block">Personalización de Asesoría</span>
        <h2 class="text-2xl font-bold text-gray-1 dark:text-slate-200 mt-1 mb-2 font-header">Cuéntanos sobre tu empresa</h2>
        <p class="text-sm text-gray-2 dark:text-slate-400">Para asignarte al consultor experto ideal para tu caso.</p>
      </div>

      <!-- Barra de progreso -->
      <div id="wa-modal-progress" class="flex gap-1.5 my-6"></div>

      <!-- Steps container -->
      <div id="wa-modal-steps" style="transition: opacity 0.35s ease; opacity: 1;"></div>

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
        { value: 'pequena', icon: 'fa-store',     label: 'Pequeña',  sub: 'De 1 a 10 empleados' },
        { value: 'mediana', icon: 'fa-building',  label: 'Mediana / Grande',  sub: 'Más de 10 empleados' }
      ]
    },
    {
      key: 'goal',
      question: '¿Qué área buscas automatizar con IA?',
      options: [
        { value: 'ventas', icon: 'fa-comments',          label: 'Ventas y Atención',   sub: 'Chatbots, WhatsApp, CRM' },
        { value: 'operaciones', icon: 'fa-gears',        label: 'Operaciones',  sub: 'Procesos internos, Datos, Agentes' }
      ]
    },
    {
      key: 'crm',
      question: '¿Cómo gestionan a sus clientes hoy?',
      options: [
        { value: 'crm',  icon: 'fa-laptop-code',        label: 'Usamos un CRM',  sub: 'Hubspot, Kommo, Salesforce, etc.' },
        { value: 'excel',  icon: 'fa-file-excel',       label: 'Excel / Manual',  sub: 'Hojas de cálculo, WhatsApp manual' }
      ]
    },
    {
      key: 'urgency',
      question: '¿Cuál es tu nivel de urgencia?',
      options: [
        { value: 'pronto', icon: 'fa-bolt', label: 'Lo necesito pronto',       sub: 'Quiero implementarlo este mes' },
        { value: 'explorando', icon: 'fa-compass', label: 'Estoy explorando',  sub: 'Busco información y opciones' }
      ]
    }
  ];

  const totalSteps = steps.length;

  // ─── Helpers ────────────────────────────────────────────────────────────────
  function buildProgressBar() {
    const bar = document.getElementById('wa-modal-progress');
    bar.innerHTML = '';
    for (let i = 0; i < totalSteps; i++) {
      const seg = document.createElement('div');
      seg.className = 'h-1.5 rounded-full flex-1 transition-colors duration-300 ' +
        (i <= currentStep ? 'bg-brand dark:bg-brand-light' : 'bg-gray-200 dark:bg-zinc-800');
      bar.appendChild(seg);
    }
  }

  function buildStepHTML(step) {
    return `
      <h3 class="text-xl font-bold text-gray-1 dark:text-slate-200 mb-5 text-center">${step.question}</h3>
      <div class="flex flex-col sm:flex-row gap-3">
        ${step.options.map(opt => `
          <button class="wa-modal-opt flex-1 bg-white dark:bg-zinc-900 hover:bg-gray-50 dark:hover:bg-zinc-800 border border-gray-200 dark:border-zinc-800 rounded-2xl p-5 transition-all text-center group hover:border-brand dark:hover:border-brand" data-key="${step.key}" data-val="${opt.value}">
            <i class="fas ${opt.icon} text-3xl text-gray-2 dark:text-slate-500 group-hover:text-brand dark:group-hover:text-brand-light mb-3 transition-colors block mx-auto"></i>
            <span class="block font-bold text-lg text-gray-1 dark:text-slate-200 mb-1">${opt.label}</span>
            <span class="text-xs text-gray-2 dark:text-slate-400 leading-tight block">${opt.sub}</span>
          </button>`).join('')}
      </div>`;
  }

  function attachStepListeners(step) {
    document.getElementById('wa-modal-steps').querySelectorAll('.wa-modal-opt').forEach(btn => {
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
    container.style.opacity = '0';

    setTimeout(function () {
      buildProgressBar();
      container.innerHTML = buildStepHTML(steps[currentStep]);
      attachStepListeners(steps[currentStep]);
      void container.offsetHeight; // trigger reflow
      container.style.opacity = '1';
      isAnimating = false;
    }, 300);
  }

  function renderStep() {
    buildProgressBar();
    const container = document.getElementById('wa-modal-steps');
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

    let msg = '\\n\\n📋 *Perfil de Empresa:*\\n';
    msg += `🏢 Tamaño: ${labels.size[state.size] || state.size}\\n`;
    msg += `🎯 Objetivo principal: ${labels.goal[state.goal] || state.goal}\\n`;
    msg += `💻 Gestión actual: ${labels.crm[state.crm] || state.crm}\\n`;
    msg += `⏱️ Urgencia: ${labels.urgency[state.urgency] || state.urgency}`;
    return msg;
  }

  function finalize() {
    let finalUrl = pendingHref;
    
    try {
      const urlObj = new URL(pendingHref);
      let currentText = urlObj.searchParams.get('text') || '';
      const msg = buildMessage();
      urlObj.searchParams.set('text', currentText + msg);
      finalUrl = urlObj.toString();
    } catch (e) {
      // Si la URL no es válida (ej. falla parseo), hacemos un append tonto
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
    const card = document.getElementById('wa-modal-card');
    
    overlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    // Animación de entrada
    requestAnimationFrame(() => {
      card.classList.remove('scale-95', 'opacity-0');
      card.classList.add('scale-100', 'opacity-100');
    });
  }

  function closeModal() {
    const overlay = document.getElementById('wa-modal-overlay');
    const card = document.getElementById('wa-modal-card');
    
    card.classList.remove('scale-100', 'opacity-100');
    card.classList.add('scale-95', 'opacity-0');
    
    setTimeout(() => {
      overlay.style.display = 'none';
      document.body.style.overflow = '';
    }, 300);
  }

  // Cerrar con × o backdrop
  document.getElementById('wa-modal-close').addEventListener('click', function () {
    closeModal();
    if (pendingHref) window.open(pendingHref, '_blank'); // Si cierran, al menos enviamos a WhatsApp
  });
  
  document.getElementById('wa-modal-backdrop').addEventListener('click', function () {
    closeModal();
    if (pendingHref) window.open(pendingHref, '_blank');
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
