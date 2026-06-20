import os
import csv
import json
from urllib.parse import quote
import shutil
import random
import re
from industry_data import INDUSTRY_DATA
from jargon_data import JARGON_DICT

# Config
SRC_DIR = "templates"
DIST_DIR = "dist"
CSV_FILE = "programatic.csv"
PILLARS_CSV = "pillars.csv"
WA_NUMERO = "573151206985" # Phone Number

def spin_text(text):
    """
    Parses standard spintax like {option1|option2|option3}.
    Allows nested spintax recursively.
    """
    def replacer(match):
        options = match.group(1).split('|')
        return random.choice(options)
    
    pattern = re.compile(r'\{([^{}]+)\}')
    while pattern.search(text):
        text = pattern.sub(replacer, text)
    return text

def build_local_context(row):
    ciudad = row.get('Ciudad', '')
    demonimo = row.get('Demónimo', 'habitantes')
    if not demonimo:
        demonimo = 'ciudadanos'
    
    barrios_str = row.get('Barrios', '')
    barrios = [b.strip() for b in barrios_str.split('|') if b.strip()]
    
    barrio1 = barrios[0] if len(barrios) > 0 else 'el centro'
    barrio2 = barrios[1] if len(barrios) > 1 else 'las afueras'
    
    industria = row.get('Industria', 'negocios')
    dolor = row.get('Dolor_Principal', 'perder ventas')
    
    templates = [
        f"Sabemos que los {demonimo} son {{exigentes|impacientes|clientes que buscan rapidez}}. Por eso, desde {barrio1} hasta {barrio2}, los dueños de {industria} ya están {{automatizando su atención|implementando asistentes de IA|delegando la atención a bots}} para resolver problemas como: {dolor}.",
        f"En {ciudad}, la competencia es {{feroz|fuerte|alta}}. Los negocios en {barrio1} y zonas cercanas saben que los {demonimo} no esperan. Implementar un Agente IA es la mejor forma de {{resolver|eliminar}} problemas como: {dolor}.",
        f"Desde {barrio1} hasta {barrio2}, hemos notado que los {demonimo} prefieren {{respuestas inmediatas|comprar por WhatsApp|atención 24/7}}. Si tu negocio aún tiene este problema, un Agente IA es el siguiente paso."
    ]
    
    return spin_text(random.choice(templates))

def build_testimonials_html(row):
    """Genera un marquee CSS con nombres de negocios y estrellas para validar AggregateRating."""
    ciudad = row.get('Ciudad', '')
    industria_singular = row.get('Industria_Singular', 'negocio')
    industria = row.get('Industria', 'Negocios')
    cliente_negocio = row.get('Cliente_Negocio', '')
    cliente_barrio = row.get('Cliente_Barrio', '')
    barrios_str = row.get('Barrios', '')
    barrios = [b.strip() for b in barrios_str.split('|') if b.strip()]

    # Generar variaciones de nombres de negocios ficticios
    prefixes = ['Centro', 'Grupo', 'Soluciones', 'Red', 'Punto', 'Club', 'Studio']
    suffixes = ['Express', 'Plus', 'Pro', 'Digital', 'Premium', 'Hub', 'Lab']
    items = []

    # 1. Usar el dato real si existe
    if cliente_negocio:
        barrio_txt = f' en {cliente_barrio}' if cliente_barrio else ''
        items.append(f'{cliente_negocio}{barrio_txt}')

    # 2. Generar combinaciones variadas con barrios
    seed_names = [
        f'{random.choice(prefixes)} {industria_singular} {ciudad}',
        f'{industria_singular} {random.choice(suffixes)} {ciudad}',
        f'{random.choice(prefixes)} {industria} {random.choice(suffixes)}',
    ]
    for name in seed_names:
        items.append(name)

    # 3. Agregar variaciones con barrios reales
    for i, barrio in enumerate(barrios[:3]):
        items.append(f'{industria_singular} {barrio}')

    # 4. Completar hasta 8 items mínimo
    extras = [
        f'{industria_singular} {ciudad} Centro',
        f'Asesores {industria} {ciudad}',
        f'{industria_singular} Integral {ciudad}',
    ]
    for extra in extras:
        if len(items) < 8:
            items.append(extra)

    # Generar los spans del marquee
    stars = '⭐⭐⭐⭐⭐'
    spans = ''
    for item in items:
        spans += f'<span class="testimonial-item">{stars} {item}</span>\n'

    # Duplicar para efecto seamless
    marquee_content = spans + spans

    html = f'''<section class="py-6 overflow-hidden border-y border-gray-100 dark:border-zinc-800/50 bg-[#FDFBF7]/50 dark:bg-zinc-900/50" aria-label="Reseñas de clientes">
    <style>
        @keyframes marquee-scroll {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-50%); }}
        }}
        .marquee-track {{
            display: flex;
            width: max-content;
            animation: marquee-scroll 35s linear infinite;
        }}
        .marquee-track:hover {{
            animation-play-state: paused;
        }}
        .testimonial-item {{
            display: inline-flex;
            align-items: center;
            white-space: nowrap;
            padding: 8px 24px;
            margin: 0 8px;
            font-size: 14px;
            font-weight: 500;
            color: #52525b;
            border-radius: 9999px;
            background: rgba(255,255,255,0.7);
            border: 1px solid #e4e4e7;
            backdrop-filter: blur(4px);
            transition: all 0.3s ease;
        }}
        .dark .testimonial-item {{
            color: #a1a1aa;
            background: rgba(39,39,42,0.5);
            border-color: #3f3f46;
        }}
        .testimonial-item:hover {{
            border-color: #10b981;
            color: #18181b;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(16,185,129,0.1);
        }}
        .dark .testimonial-item:hover {{
            color: #f4f4f5;
            border-color: #34d399;
        }}
    </style>
    <div class="marquee-track">
        {marquee_content}
    </div>
</section>'''
    return html


def build_demo_interactiva_html(row):
    """Genera el HTML y JavaScript de la demo interactiva del chat de WhatsApp y el calendario."""
    import datetime
    import json
    
    ciudad = row.get('Ciudad', '')
    industria = row.get('Industria', 'Negocios')
    industria_singular = row.get('Industria_Singular', 'negocio')
    cliente_negocio = row.get('Cliente_Negocio', 'Consultor IA')
    pais = row.get('País', 'Colombia')
    demonimo = row.get('Demónimo', 'habitantes')
    barrios = row.get('Barrios', '')
    dolor = row.get('Dolor_Principal', 'perder ventas')
    solucion = row.get('Solución_Clave', 'automatizar las respuestas')
    
    dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    today_obj = datetime.date.today()
    day_of_week = dias_semana[today_obj.weekday()]
    today_str = today_obj.strftime('%Y-%m-%d')
    today_formatted = today_obj.strftime('%d de %B de %Y')
    
    # Generar tabla de correspondencia de días de la semana y fechas para los próximos 8 días
    ref_dias = []
    temp_ref = today_obj
    for i in range(8):
        ref_dias.append(f"  * {dias_semana[temp_ref.weekday()]} es {temp_ref.strftime('%Y-%m-%d')}")
        temp_ref += datetime.timedelta(days=1)
    proximos_dias_str = "\n".join(ref_dias)
    
    # Prompt inicial del bot
    bot_initial_msg = f"¡Hola! Bienvenido a {cliente_negocio} en {ciudad}. Soy su Asistente Virtual Inteligente. ¿Le gustaría agendar una cita o visita, o prefiere conocer nuestros servicios?"
    
    # System Prompt para el modelo de OpenRouter
    system_prompt = f"""Eres el Agente de Inteligencia Artificial oficial de '{cliente_negocio}' en la ciudad de '{ciudad}', '{pais}'.
Tu industria es '{industria_singular}'.
Tu objetivo principal es convencer al usuario de agendar una cita o visita de negocios.
Debes sonar sumamente profesional, servicial y empático (tono Tech-Luxury).
Conoce muy bien tu entorno local de '{ciudad}'. Usa de forma natural y sutil expresiones típicas de la región y menciona barrios locales como: '{barrios}' cuando hables de cobertura o ubicación.
Responde de forma muy concisa (máximo 1 o 2 oraciones, no te extiendas en párrafos largos). Este es un chat de WhatsApp de ritmo rápido.

Instrucción de agendamiento:
- Hoy es {day_of_week}, día {today_str}. Asume que el año actual es 2026.
- Tabla de referencia para saber qué fecha YYYY-MM-DD corresponde a cada día de la semana (¡USA ESTA LISTA OBLIGATORIAMENTE PARA TUS CÁLCULOS!):
{proximos_dias_str}
- Si el usuario muestra interés en agendar, coordina con él un día y una hora específicos (entre 8:00 y 18:00).
- IMPORTANTE: Una vez acordada la fecha y la hora, antes de confirmar la cita, DEBES pedirle obligatoriamente su nombre y correo electrónico (ej: "Para registrar la cita en la agenda del negocio, por favor confírmeme su nombre completo y su dirección de correo electrónico").
- Solo después de que el usuario te proporcione su nombre y correo electrónico (no importa el orden o formato), debes dar el mensaje final de confirmación de la cita.
- AL FINAL de tu mensaje de confirmación, y ÚNICAMENTE en ese mensaje, debes agregar EXACTAMENTE esta marca especial para que el sistema registre la cita en el calendario:
[CONFIRMAR_CITA: YYYY-MM-DD HH:MM | NOMBRE | EMAIL]
Sustituyendo YYYY-MM-DD por la fecha exacta calculada (ej: 2026-06-25), HH:MM por la hora (ej: 10:30), NOMBRE por el nombre completo facilitado por el usuario y EMAIL por su correo electrónico.
Ejemplo de mensaje final: "¡Perfecto, Juan! Tu cita ha quedado agendada para el viernes 19 de junio a las 14:00. Hemos enviado la confirmación a juan@gmail.com. [CONFIRMAR_CITA: 2026-06-19 14:00 | Juan Pérez | juan@gmail.com]"
No uses markdown ni negritas en la marca especial. Escríbela tal cual.
"""

    html = '''
    <section id="demo-interactiva" class="py-24 bg-gradient-to-b from-[#FDFBF7]/40 to-white dark:from-zinc-950 dark:to-zinc-900 border-t border-gray-200/50 dark:border-zinc-800/80 relative overflow-hidden">
        <!-- Estilos CSS personalizados para la Demo Premium -->
        <style>
            @keyframes demo-shimmer {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
            .animate-shimmer {
                animation: demo-shimmer 2.5s infinite linear;
            }
            /* Suavizar la navegación del calendario */
            #calendar-prev-btn, #calendar-next-btn {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            /* Scrollbar premium minimalista para las horas */
            #time-slots-container::-webkit-scrollbar {
                width: 4px;
            }
            #time-slots-container::-webkit-scrollbar-track {
                background: transparent;
            }
            #time-slots-container::-webkit-scrollbar-thumb {
                background: #e4e4e7;
                border-radius: 9999px;
            }
            .dark #time-slots-container::-webkit-scrollbar-thumb {
                background: #3f3f46;
            }
            /* Estilo Premium de Botones de Respuesta Rápida */
            .quick-reply-btn {
                background-color: #ffffff;
                color: #075E54;
                border: 1px solid rgba(7, 94, 84, 0.15);
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .quick-reply-btn:hover {
                background-color: rgba(7, 94, 84, 0.04);
                border-color: #075E54;
                transform: translateY(-1px);
                box-shadow: 0 4px 10px rgba(7, 94, 84, 0.12);
            }
            .quick-reply-btn:active {
                transform: scale(0.95);
            }
            
            /* Modo Oscuro Premium */
            .dark .quick-reply-btn {
                background-color: rgba(0, 168, 132, 0.08);
                color: #00e676;
                border-color: rgba(0, 230, 118, 0.2);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }
            .dark .quick-reply-btn:hover {
                background-color: rgba(0, 230, 118, 0.18);
                border-color: #00e676;
                color: #ffffff;
                box-shadow: 0 0 14px rgba(0, 230, 118, 0.4);
                transform: translateY(-1px);
            }
            .dark .quick-reply-btn:active {
                transform: scale(0.95);
            }
            /* Clases responsivas personalizadas para evitar conflictos de especificidad de Tailwind */
            @media (max-width: 1023px) {
                .hidden-mobile {
                    display: none !important;
                }
                .visible-mobile-flex {
                    display: flex !important;
                }
                /* Ajustes de tamaño del calendario para móviles */
                .calendar-container {
                    padding: 14px !important;
                    gap: 12px !important;
                }
                #calendar-days-grid {
                    gap: 4px !important;
                }
                #calendar-days-grid button {
                    width: 32px !important;
                    height: 32px !important;
                    font-size: 11px !important;
                }
                #calendar-left-col h3 {
                    font-size: 14px !important;
                }
                #calendar-left-col p {
                    font-size: 9px !important;
                }
                /* Compactación del Chat en móvil */
                #demo-chat-body {
                    padding: 10px !important;
                }
                #demo-chat-body > div {
                    font-size: 13px !important;
                    padding: 8px 12px !important;
                    margin-bottom: 2px !important;
                }
                .lg\:col-span-5 .shrink-0 {
                    padding: 8px 12px !important;
                }
                .lg\:col-span-5 h4 {
                    font-size: 13px !important;
                }
                .lg\:col-span-5 p {
                    font-size: 10px !important;
                }
                #chat-quick-replies {
                    padding: 6px 12px !important;
                }
                #chat-quick-replies button {
                    font-size: 10px !important;
                    padding: 5px 10px !important;
                }
            }
            /* Carrusel horizontal de slots de hora en móvil */
            @media (max-width: 639px) {
                #time-slots-container {
                    display: flex !important;
                    flex-direction: row !important;
                    flex-wrap: nowrap !important;
                    overflow-x: auto !important;
                    padding-bottom: 8px !important;
                    gap: 8px !important;
                    scrollbar-width: none !important;
                    -ms-overflow-style: none !important;
                }
                #time-slots-container::-webkit-scrollbar {
                    display: none !important;
                }
                #time-slots-container button {
                    flex-shrink: 0 !important;
                    min-width: 72px !important;
                    padding: 6px 12px !important;
                    font-size: 11px !important;
                }
            }
        </style>


        <!-- Blobs decorativos -->
        <div class="absolute -top-[10%] -left-[10%] w-[30vw] h-[30vw] rounded-full bg-accent/5 dark:bg-accent/10 blur-[100px] pointer-events-none"></div>
        <div class="absolute -bottom-[10%] -right-[10%] w-[30vw] h-[30vw] rounded-full bg-success/5 dark:bg-success/10 blur-[100px] pointer-events-none"></div>
        
        <div class="container mx-auto px-4 max-w-6xl relative z-10">
            <div class="flex flex-col lg:flex-row items-center justify-between gap-8 mb-16 border-b border-gray-150/40 dark:border-zinc-800/60 pb-12">
                <div class="lg:w-7/12 text-left">
                    <span class="inline-flex items-center gap-1.5 bg-[#2563eb]/10 dark:bg-[#2563eb]/20 text-accent dark:text-[#53bdeb] px-4 py-1.5 rounded-full text-xs font-semibold uppercase tracking-wider mb-3">
                        <i class="fas fa-play-circle"></i> Demo Interactiva en Vivo
                    </span>
                    <h2 class="text-3xl md:text-5xl font-header font-bold mb-6">No parecemos un bot de menú aburrido</h2>
                    <p class="text-lg text-zinc-600 dark:text-zinc-400 leading-relaxed">
                        Tus clientes odian presionar el "1" o el "2". El Agente de IA para __INDUSTRIA_SINGULAR__ de __CLIENTE_NEGOCIO__ conversa de forma 100% natural: <strong>entiende notas de voz, tolera errores al escribir y agenda de forma autónoma.</strong>
                    </p>
                </div>
                <div class="lg:w-5/12 w-full">
                    <ul class="space-y-3.5 text-zinc-700 dark:text-zinc-300 font-semibold text-sm">
                        <li class="flex items-center gap-3"><i class="fas fa-heart text-[#00a884] dark:text-[#00a884] text-lg shrink-0"></i> Tono conversacional y cálido</li>
                        <li class="flex items-center gap-3"><i class="fas fa-microphone text-[#00a884] dark:text-[#00a884] text-lg shrink-0"></i> Transcribe y entiende audios (notas de voz)</li>
                        <li class="flex items-center gap-3"><i class="fas fa-spell-check text-[#00a884] dark:text-[#00a884] text-lg shrink-0"></i> Tolera jergas y errores de ortografía</li>
                        <li class="flex items-center gap-3"><i class="fas fa-image text-[#00a884] dark:text-[#00a884] text-lg shrink-0"></i> Soporta imágenes y procesamiento visual</li>
                    </ul>
                    <div class="mt-4 p-3 bg-zinc-50 dark:bg-zinc-900/50 border border-zinc-200/60 dark:border-zinc-800/80 rounded-2xl text-[11px] text-zinc-500 dark:text-zinc-400 flex items-center gap-2">
                        <i class="fas fa-info-circle text-[#00a884] shrink-0 text-sm"></i>
                        <span><strong>¡Pónlo a prueba!</strong> Escríbele al chat de abajo con mala ortografía o dile "quiero agendar cita" para ver el resultado en el calendario de la derecha.</span>
                    </div>
                </div>
            </div>
            
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 lg:gap-8 items-stretch">
                <!-- Columna Izquierda: Chat de WhatsApp Mockup -->
                <div class="lg:col-span-5 w-full flex flex-col h-[360px] lg:h-[600px] lg:max-h-[600px] lg:min-h-[600px]">
                    <div class="flex-1 bg-[#efeae2] dark:bg-[#0b141a] rounded-3xl border border-gray-200 dark:border-zinc-800 shadow-2xl overflow-hidden flex flex-col relative h-full max-h-full">
                        <!-- WhatsApp Chat Header -->
                        <div class="bg-[#075E54] dark:bg-[#202c33] px-4 py-3 flex items-center justify-between shrink-0 relative z-10 shadow-md">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center shrink-0 overflow-hidden relative">
                                    <i class="fas fa-robot text-[#075E54] dark:text-[#8696a0] text-xl"></i>
                                </div>
                                <div>
                                    <h4 class="text-white font-medium text-sm leading-tight">Agente IA - __CLIENTE_NEGOCIO__</h4>
                                    <p id="chat-status" class="text-white/80 text-xs mt-0.5">en línea</p>
                                </div>
                            </div>
                            <div class="text-white/80 flex gap-4 text-sm">
                                <i class="fas fa-video cursor-pointer hover:text-white transition-colors"></i>
                                <i class="fas fa-phone cursor-pointer hover:text-white transition-colors"></i>
                                <i class="fas fa-ellipsis-v cursor-pointer hover:text-white transition-colors"></i>
                            </div>
                        </div>
                        
                        <!-- Chat Body -->
                        <div id="demo-chat-body" class="flex-1 overflow-y-auto p-4 flex flex-col gap-3 relative z-10">
                            <!-- Background Pattern overlay -->
                            <div class="absolute inset-0 opacity-[0.12] dark:opacity-[0.03] bg-[url('https://i.pinimg.com/736x/8c/98/99/8c98994518b575bfd8c949e91d20548b.jpg')] bg-cover bg-center pointer-events-none z-0"></div>
                        </div>
                        
                        <!-- Botones de Respuesta Rápida (Quick Replies) -->
                        <div id="chat-quick-replies" class="px-4 py-2.5 bg-[#f0f2f5]/90 dark:bg-[#1f2c34]/90 flex flex-wrap gap-2 justify-center border-t border-gray-200/20 dark:border-zinc-800/30 relative z-20 transition-all duration-300">
                            <button id="btn-quick-reply-1" class="quick-reply-btn text-xs font-bold px-3.5 py-2 rounded-full cursor-pointer flex items-center gap-1.5">
                                👋 Decir "Hola"
                            </button>
                            <button id="btn-quick-reply-2" class="quick-reply-btn text-xs font-bold px-3.5 py-2 rounded-full cursor-pointer flex items-center gap-1.5">
                                📅 Agendar Cita
                            </button>
                        </div>
                        
                        <!-- Chat Input Box -->
                        <div class="p-3 bg-[#f0f2f5] dark:bg-[#1f2c34] flex items-center gap-3 border-t border-gray-200/50 dark:border-zinc-800/80 shrink-0 relative z-10">
                            <button class="text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 text-lg">
                                <i class="far fa-laugh"></i>
                            </button>
                            <button class="text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 text-lg">
                                <i class="fas fa-plus"></i>
                            </button>
                            <input type="text" id="demo-chat-input" placeholder="Escribe un mensaje..." class="flex-1 bg-white dark:bg-[#2a3942] text-zinc-800 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 px-4 py-2.5 rounded-xl border-none focus:outline-none focus:ring-1 focus:ring-[#075E54] text-sm" />
                            <button id="demo-chat-send-btn" class="w-10 h-10 rounded-full bg-[#00a884] dark:bg-[#00a884] text-white flex items-center justify-center hover:bg-[#008f72] transition-colors shadow-md">
                                <i class="fas fa-paper-plane text-xs"></i>
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Columna Derecha: Calendario y Disponibilidad -->
                <div class="lg:col-span-7 w-full flex flex-col h-auto min-h-[380px] lg:h-[600px] lg:min-h-[600px] lg:max-h-[600px]">
                    <div class="calendar-container flex-1 bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded-3xl p-5 sm:p-6 shadow-2xl flex flex-col lg:flex-row gap-6 h-full lg:max-h-full relative overflow-hidden">
                        <!-- Alerta de Confirmación de Cita -->
                        <div id="booking-success-alert" class="absolute inset-x-4 top-4 z-50 bg-[#e6fffa]/95 dark:bg-[#004d40]/75 backdrop-blur-md border border-[#b2f5ea] dark:border-[#00796b]/60 text-[#134e4a] dark:text-[#b2f5ea] p-3 sm:p-4 rounded-2xl flex items-center gap-3 shadow-xl transform -translate-y-4 opacity-0 pointer-events-none transition-all duration-500">
                            <div class="w-10 h-10 rounded-full bg-[#319795] text-white flex items-center justify-center shrink-0">
                                <i class="fas fa-check-circle text-lg"></i>
                            </div>
                            <div>
                                <h5 class="font-bold text-sm">¡Cita Reservada con Éxito!</h5>
                                <p class="text-xs opacity-90" id="booking-alert-text">El Agente ha confirmado tu reservación en la agenda.</p>
                            </div>
                        </div>

                        <!-- Sección Izquierda: Calendario y Horas -->
                        <div id="calendar-left-col" class="flex-1 flex flex-col min-w-0 h-full justify-between">
                            <div>
                                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-gray-100 dark:border-zinc-800/80 pb-4 mb-4 gap-2">
                                    <div>
                                        <h3 class="text-base font-header font-bold text-zinc-900 dark:text-white leading-tight">Agenda de __CLIENTE_NEGOCIO__</h3>
                                        <p class="text-[10px] text-zinc-500 dark:text-zinc-400">Demostración en tiempo real</p>
                                    </div>
                                    <div class="flex items-center gap-3 shrink-0">
                                        <div class="flex items-center gap-1.5">
                                            <span class="w-2.5 h-2.5 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 inline-block shadow-sm shadow-blue-500/20"></span>
                                            <span class="text-[9px] font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">Seleccionado</span>
                                        </div>
                                        <div class="flex items-center gap-1.5">
                                            <span class="w-2.5 h-2.5 rounded-full bg-gradient-to-br from-emerald-400 to-teal-600 inline-block shadow-sm shadow-emerald-500/10"></span>
                                            <span class="text-[9px] font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">Reservado</span>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Calendario Header (Mes y Navegación) -->
                                <div class="flex items-center justify-between mb-3">
                                    <span id="calendar-month-year" class="font-bold text-sm text-zinc-800 dark:text-zinc-200 tracking-tight">Junio 2026</span>
                                    <div class="flex gap-1.5">
                                        <button id="calendar-prev-btn" class="w-7 h-7 rounded-full border border-gray-200/60 dark:border-zinc-800/80 flex items-center justify-center hover:bg-gray-50 dark:hover:bg-zinc-800/80 hover:border-blue-500 dark:hover:border-blue-400 transition-all text-zinc-500 dark:text-zinc-400 active:scale-90 focus:outline-none">
                                            <i class="fas fa-chevron-left text-[8px]"></i>
                                        </button>
                                        <button id="calendar-next-btn" class="w-7 h-7 rounded-full border border-gray-200/60 dark:border-zinc-800/80 flex items-center justify-center hover:bg-gray-50 dark:hover:bg-zinc-800/80 hover:border-blue-500 dark:hover:border-blue-400 transition-all text-zinc-500 dark:text-zinc-400 active:scale-90 focus:outline-none">
                                            <i class="fas fa-chevron-right text-[8px]"></i>
                                        </button>
                                    </div>
                                </div>
                                
                                <!-- Calendario Días de la Semana -->
                                <div class="grid grid-cols-7 gap-1 text-center text-[10px] font-bold text-zinc-400 dark:text-zinc-500 mb-2.5 tracking-wider uppercase select-none">
                                    <span>DOM</span><span>LUN</span><span>MAR</span><span>MIÉ</span><span>JUE</span><span>VIE</span><span>SÁB</span>
                                </div>
                                
                                <!-- Calendario Celdas (Días del Mes) -->
                                <div id="calendar-days-grid" class="grid grid-cols-7 gap-1 text-center text-xs font-semibold mb-3">
                                    <!-- Inyectado dinámicamente -->
                                </div>
                            </div>
                            
                            <!-- Panel de Horas del Día Seleccionado -->
                            <div class="border-t border-gray-100 dark:border-zinc-800/80 pt-4 shrink-0">
                                <h4 id="selected-day-label" class="font-bold text-xs text-zinc-800 dark:text-zinc-200 mb-2.5">Disponibilidad:</h4>
                                <div id="time-slots-container" class="grid grid-cols-3 sm:grid-cols-4 gap-2 max-h-[110px] overflow-y-auto pr-1">
                                    <!-- Inyectado dinámicamente -->
                                </div>
                            </div>
                        </div>
                        
                        <!-- Sección Derecha: Estado de la Reserva y Animación -->
                        <div id="calendar-right-col" class="hidden-mobile lg:flex w-full lg:w-56 border-t lg:border-t-0 lg:border-l border-gray-100 dark:border-zinc-800/80 pt-4 lg:pt-0 lg:pl-4 flex-col shrink-0 lg:h-full">
                            <h4 class="font-bold text-xs text-zinc-800 dark:text-zinc-200 mb-2 shrink-0">Estado de Reserva</h4>
                            <div id="booking-status-card" class="w-full h-auto min-h-[160px] lg:flex-1 flex flex-col items-center justify-center text-center p-4 rounded-3xl bg-zinc-50/50 dark:bg-zinc-950/30 border border-dashed border-zinc-200 dark:border-zinc-800/80 transition-all duration-500 overflow-hidden relative">
                                <!-- Estado Inicial (Vacío) -->
                                <div id="booking-status-empty" class="flex flex-col items-center py-4">
                                    <div class="w-10 h-10 rounded-full bg-blue-50 dark:bg-blue-900/20 text-blue-500 dark:text-blue-400 flex items-center justify-center mb-2 animate-pulse">
                                        <i class="far fa-calendar-alt text-base"></i>
                                    </div>
                                    <p class="text-xs font-bold text-zinc-500 dark:text-zinc-400 leading-tight">Sin Reservas</p>
                                    <p class="text-[9px] text-zinc-400 dark:text-zinc-500 mt-1 max-w-[150px]">Pide una cita al chatbot facilitando fecha, hora, nombre y correo.</p>
                                </div>
                                <!-- Estado Confirmado (Oculto al inicio) -->
                                <div id="booking-status-success" class="hidden w-full flex-col items-center">
                                    <!-- Checkmark animado -->
                                    <div class="w-12 h-12 rounded-full bg-gradient-to-br from-emerald-400 to-teal-500 text-white flex items-center justify-center mb-3 shadow-lg shadow-emerald-500/20 transform scale-0 transition-all duration-500 ease-out ring-8 ring-emerald-500/10 dark:ring-emerald-400/10 relative" id="success-checkmark">
                                        <div class="absolute inset-0 rounded-full ring-8 ring-emerald-500/10 animate-pulse"></div>
                                        <i class="fas fa-check text-lg"></i>
                                    </div>
                                    <span class="inline-flex items-center gap-1.5 bg-gradient-to-r from-emerald-500 to-teal-600 text-white text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-3.5 border border-emerald-400/20 shadow-sm relative overflow-hidden">
                                        <span class="absolute inset-0 w-[200%] h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full animate-shimmer" style="animation: demo-shimmer 2.5s infinite linear;"></span>
                                        <i class="fas fa-lock text-[8px]"></i> Lugar Bloqueado
                                    </span>
                                    
                                    <!-- Detalles del ticket -->
                                    <div class="w-full bg-white dark:bg-zinc-800 border border-gray-150 dark:border-zinc-700/60 rounded-2xl p-4 text-left text-[11px] space-y-2.5 shadow-md relative overflow-hidden">
                                        <!-- Cutouts left & right -->
                                        <div class="absolute top-[48%] -left-1.5 w-3 h-3 bg-gradient-to-br from-[#f4fbf9] to-[#edfcf8] dark:from-[#0b1b17] dark:to-[#091a16] rounded-full border-r border-emerald-100 dark:border-emerald-800/35"></div>
                                        <div class="absolute top-[48%] -right-1.5 w-3 h-3 bg-gradient-to-br from-[#f4fbf9] to-[#edfcf8] dark:from-[#0b1b17] dark:to-[#091a16] rounded-full border-l border-emerald-100 dark:border-emerald-800/35"></div>
                                        
                                        <div class="flex justify-between border-b border-gray-50 dark:border-zinc-800/30 pb-1.5">
                                            <span class="text-zinc-400 font-medium">Cliente:</span>
                                            <span class="font-bold text-zinc-800 dark:text-zinc-200 truncate max-w-[110px]" id="ticket-name">-</span>
                                        </div>
                                        <div class="flex justify-between border-b border-gray-50 dark:border-zinc-800/30 pb-1.5">
                                            <span class="text-zinc-400 font-medium">Email:</span>
                                            <span class="font-bold text-zinc-800 dark:text-zinc-200 truncate max-w-[110px]" id="ticket-email">-</span>
                                        </div>
                                        
                                        <!-- Dashed separator aligned with cutouts -->
                                        <div class="border-t border-dashed border-gray-250 dark:border-zinc-700/50 my-2"></div>
                                        
                                        <div class="flex justify-between border-b border-gray-50 dark:border-zinc-800/30 pb-1.5">
                                            <span class="text-zinc-400 font-medium">Fecha:</span>
                                            <span class="font-bold text-zinc-800 dark:text-zinc-200" id="ticket-date">-</span>
                                        </div>
                                        <div class="flex justify-between">
                                            <span class="text-zinc-400 font-medium">Hora:</span>
                                            <span class="font-bold text-emerald-500 dark:text-emerald-400 text-xs" id="ticket-time">-</span>
                                        </div>
                                    </div>
                                    <p class="text-[9px] text-zinc-400 dark:text-zinc-500 mt-2 text-center">¡Cita agendada de forma autónoma!</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Tags de keywords SEO ocultos pero semánticos -->
            <div class="mt-8 text-center text-xs text-zinc-400/0 select-none pointer-events-none">
                agente de inteligencia artificial para agendamiento de citas en __CIUDAD__, automatización de reservas por whatsapp __INDUSTRIA_SINGULAR__ __CIUDAD__, chatbot inteligente para __INDUSTRIA_SINGULAR__ en __CIUDAD__, agenda virtual inteligente de __CLIENTE_NEGOCIO__.
            </div>
        </div>
        
        <!-- Script de lógica de la demo -->
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                // --- Variables Conversacionales ---
                const systemPromptB64 = "__SYSTEM_PROMPT_B64__";
                const systemPrompt = decodeURIComponent(atob(systemPromptB64).split('').map(function(c) {
                    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                }).join(''));
                let chatHistory = [
                    {"role": "system", "content": systemPrompt}
                ];
                
                const chatInput = document.getElementById("demo-chat-input");
                const chatSendBtn = document.getElementById("demo-chat-send-btn");
                const chatBody = document.getElementById("demo-chat-body");
                const chatStatus = document.getElementById("chat-status");
                
                // --- Calendario e Inicialización ---
                const dateBase = new Date(); // Año 2026, mes base
                let currentYear = 2026;
                let currentMonth = dateBase.getMonth(); // Mes actual del sistema
                const todayDay = dateBase.getDate();
                const actualMonth = dateBase.getMonth();
                const actualYear = dateBase.getFullYear();
 
                const calendarMonthYear = document.getElementById("calendar-month-year");
                const calendarDaysGrid = document.getElementById("calendar-days-grid");
                const calendarPrevBtn = document.getElementById("calendar-prev-btn");
                const calendarNextBtn = document.getElementById("calendar-next-btn");
                const selectedDayLabel = document.getElementById("selected-day-label");
                const timeSlotsContainer = document.getElementById("time-slots-container");
                
                const bookingSuccessAlert = document.getElementById("booking-success-alert");
                const bookingAlertText = document.getElementById("booking-alert-text");
                
                // Datos de disponibilidad en memoria
                // Estructura: 'YYYY-MM-DD': { 'HH:MM': { status: 'available'|'occupied'|'booked' } }
                const availabilityDb = {};
                let selectedDateStr = null;
                let confirmedBooking = null; // Guardará { date: 'YYYY-MM-DD', time: 'HH:MM' }
                
                const monthNames = [
                    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
                ];
                
                // Inicializar base de datos de disponibilidad para los próximos 60 días
                function initAvailabilityDb() {
                    const tempDate = new Date();
                    for (let d = 0; d < 60; d++) {
                        const dateStr = formatDateKey(tempDate);
                        availabilityDb[dateStr] = {};
                        
                        // Slots de 8:00 AM a 5:30 PM (bloques de 1 hora o 30 min)
                        const hours = ["08:00", "09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00"];
                        hours.forEach(h => {
                            // 60% ocupado de forma aleatoria
                            const isOccupied = Math.random() < 0.6;
                            availabilityDb[dateStr][h] = isOccupied ? 'occupied' : 'available';
                        });
                        
                        tempDate.setDate(tempDate.getDate() + 1);
                    }
                }
                
                function formatDateKey(date) {
                    const y = date.getFullYear() === actualYear ? 2026 : date.getFullYear(); // Forzar 2026 para el prompt
                    const m = String(date.getMonth() + 1).padStart(2, '0');
                    const d = String(date.getDate()).padStart(2, '0');
                    return `${y}-${m}-${d}`;
                }
 
                function formatHumanDate(dateStr) {
                    const parts = dateStr.split('-');
                    const date = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
                    return date.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long' });
                }
                
                // Renderizar el Calendario
                function renderCalendar(year, month) {
                    calendarMonthYear.textContent = `${monthNames[month]} ${year}`;
                    calendarDaysGrid.innerHTML = "";
                    
                    // Primer día del mes
                    const firstDayIdx = new Date(year, month, 1).getDay();
                    // Total de días del mes
                    const totalDays = new Date(year, month + 1, 0).getDate();
                    
                    // Rellenar celdas vacías del principio
                    const offset = new Date(year, month, 1).getDay();
                    
                    for (let i = 0; i < offset; i++) {
                        const emptyCell = document.createElement("span");
                        emptyCell.className = "text-transparent pointer-events-none";
                        emptyCell.textContent = "";
                        calendarDaysGrid.appendChild(emptyCell);
                    }
                    
                    for (let day = 1; day <= totalDays; day++) {
                        const cellDate = new Date(year, month, day);
                        const dateStr = formatDateKey(cellDate);
                        
                        const dayCell = document.createElement("button");
                        dayCell.className = "w-8 h-8 lg:w-9 lg:h-9 mx-auto rounded-full flex items-center justify-center text-xs font-semibold hover:bg-gray-100 dark:hover:bg-zinc-800 hover:scale-105 hover:shadow-sm transition-all focus:outline-none relative";
                        dayCell.textContent = day;
                        
                        // Validar si es del pasado (en base al día real actual del sistema)
                        const compareDate = new Date(actualYear, actualMonth, todayDay);
                        const cellCompare = new Date(year, month, day);
                        const isPast = cellCompare < compareDate;
                        
                        if (isPast) {
                            dayCell.className += " text-zinc-300 dark:text-zinc-700 pointer-events-none";
                        } else {
                            dayCell.className += " cursor-pointer";
                            
                            // Comprobar si hay citas confirmadas en este día en la base de datos
                            const daySlots = availabilityDb[dateStr] || {};
                            const hasBookedSlot = Object.values(daySlots).includes('booked');
                            
                            if (hasBookedSlot) {
                                dayCell.className += " bg-gradient-to-br from-emerald-400 to-teal-600 text-white shadow-md shadow-emerald-500/20";
                                
                                const badgeContainer = document.createElement("span");
                                badgeContainer.className = "absolute -top-0.5 -right-0.5 flex h-2.5 w-2.5";
                                
                                const pingDot = document.createElement("span");
                                pingDot.className = "animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75";
                                
                                const solidDot = document.createElement("span");
                                solidDot.className = "relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500 border border-white dark:border-zinc-900";
                                
                                badgeContainer.appendChild(pingDot);
                                badgeContainer.appendChild(solidDot);
                                dayCell.appendChild(badgeContainer);
                            } else if (selectedDateStr === dateStr) {
                                dayCell.className += " bg-gradient-to-br from-blue-500 to-indigo-600 text-white shadow-md shadow-blue-500/25";
                            } else {
                                dayCell.className += " text-zinc-800 dark:text-zinc-200";
                            }
                            
                            dayCell.addEventListener("click", () => {
                                selectedDateStr = dateStr;
                                selectDate(dateStr, cellDate);
                                renderCalendar(year, month);
                            });
                        }
                        
                        calendarDaysGrid.appendChild(dayCell);
                    }
                }
                
                function selectDate(dateStr, dateObj) {
                    selectedDayLabel.textContent = "Disponibilidad para el " + formatHumanDate(dateStr) + ":";
                    timeSlotsContainer.innerHTML = "";
                    
                    const slots = availabilityDb[dateStr] || {};
                    const sortedHours = Object.keys(slots).sort();
                    
                    if (sortedHours.length === 0) {
                        timeSlotsContainer.innerHTML = '<span class="text-xs text-zinc-400 col-span-4 py-2">No hay horarios definidos para esta fecha.</span>';
                        return;
                    }
                    
                    sortedHours.forEach(h => {
                        const status = slots[h];
                        const slotBtn = document.createElement("button");
                        slotBtn.className = "py-2 text-xs font-bold rounded-xl border transition-all focus:outline-none flex items-center justify-center gap-1.5 ";
                        
                        if (status === 'booked') {
                            slotBtn.className += " bg-gradient-to-r from-emerald-500 to-teal-600 border-transparent text-white shadow-md shadow-emerald-500/10 pointer-events-none";
                            slotBtn.innerHTML = '<i class="fas fa-check text-[9px]"></i> ' + h;
                        } else if (status === 'occupied') {
                            slotBtn.className += " bg-zinc-50 dark:bg-zinc-900/50 border-zinc-100 dark:border-zinc-800/80 text-zinc-300 dark:text-zinc-600 pointer-events-none";
                            slotBtn.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-zinc-300 dark:bg-zinc-700"></span>' + h;
                        } else {
                            slotBtn.className += " bg-zinc-50/50 dark:bg-zinc-900/30 border-zinc-200 dark:border-zinc-800 text-zinc-700 dark:text-zinc-300 hover:border-blue-500 dark:hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50/30 dark:hover:bg-blue-950/10 cursor-pointer";
                            slotBtn.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>' + h;
                            slotBtn.addEventListener("click", () => {
                                // Rellenar input del chat automáticamente al hacer clic en un horario libre
                                chatInput.value = "Hola, me gustaría agendar una cita para el " + formatHumanDate(dateStr) + " a las " + h;
                                chatInput.focus();
                            });
                        }
                        
                        timeSlotsContainer.appendChild(slotBtn);
                    });
                }
                
                // Controladores de botones del Calendario
                calendarPrevBtn.addEventListener("click", () => {
                    if (currentMonth === actualMonth && currentYear === 2026) return; // No ir al pasado
                    currentMonth--;
                    if (currentMonth < 0) {
                        currentMonth = 11;
                        currentYear--;
                    }
                    renderCalendar(currentYear, currentMonth);
                });
                
                calendarNextBtn.addEventListener("click", () => {
                    currentMonth++;
                    if (currentMonth > 11) {
                        currentMonth = 0;
                        currentYear++;
                    }
                    renderCalendar(currentYear, currentMonth);
                });
                
                // --- Lógica del Chat ---
                function getAvailabilityContext() {
                    let ctx = `\n\nDISPONIBILIDAD REAL EN TIEMPO REAL (Usa esta información para responder si te preguntan por citas, o si un horario está ocupado; ofrece alternativas libres de esta lista):\n`;
                    const tempDate = new Date();
                    for (let i = 0; i < 5; i++) {
                        const dateStr = formatDateKey(tempDate);
                        const slots = availabilityDb[dateStr] || {};
                        const freeSlots = [];
                        const busySlots = [];
                        Object.keys(slots).forEach(h => {
                            if (slots[h] === 'available') {
                                freeSlots.push(h);
                            } else {
                                busySlots.push(h);
                            }
                        });
                        const dateHuman = formatHumanDate(dateStr);
                        ctx += `- ${dateHuman} (${dateStr}): Libres: [${freeSlots.join(", ")}]. Ocupados: [${busySlots.join(", ")}].\n`;
                        tempDate.setDate(tempDate.getDate() + 1);
                    }
                    return ctx;
                }

                function appendMessage(sender, text, timestamp) {
                    const msgDiv = document.createElement("div");
                    const time = timestamp || new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
                    
                    if (sender === 'user') {
                        msgDiv.className = "relative z-10 max-w-[85%] self-end bg-[#d9fdd3] dark:bg-[#005c4b] text-zinc-800 dark:text-[#e9edef] px-4 py-2.5 rounded-2xl rounded-tr-none shadow-sm text-sm leading-snug";
                        msgDiv.innerHTML = text + `<span class="text-[9px] text-zinc-400 block text-right mt-1">${time} <i class="fas fa-check-double text-blue-400 ml-1"></i></span>`;
                    } else {
                        msgDiv.className = "relative z-10 max-w-[85%] self-start bg-white dark:bg-[#202c33] text-zinc-800 dark:text-[#e9edef] px-4 py-2.5 rounded-2xl rounded-tl-none shadow-sm text-sm leading-snug border border-gray-100 dark:border-zinc-800/80";
                        msgDiv.innerHTML = text + `<span class="text-[9px] text-zinc-400 block text-right mt-1">${time}</span>`;
                    }
                    
                    chatBody.appendChild(msgDiv);
                    chatBody.scrollTop = chatBody.scrollHeight;
                }
                
                async function sendMessage() {
                    const messageText = chatInput.value.trim();
                    if (!messageText) return;
                    
                    const quickRepliesContainer = document.getElementById("chat-quick-replies");
                    if (quickRepliesContainer) {
                        quickRepliesContainer.style.display = "none";
                    }
                    
                    appendMessage('user', messageText);
                    chatInput.value = "";
                    
                    // Mostrar "Escribiendo..." en el estado del header
                    chatStatus.textContent = "escribiendo...";
                    chatStatus.className = "text-emerald-400 font-semibold animate-pulse text-xs mt-0.5";
                    
                    // Guardar en el historial
                    chatHistory.push({"role": "user", "content": messageText});
                    
                    // Actualizar el primer mensaje de system con la disponibilidad real actual
                    chatHistory[0].content = systemPrompt + getAvailabilityContext();
                    
                    // Crear e insertar burbuja de "escribiendo..." en el cuerpo del chat
                    const typingDiv = document.createElement("div");
                    typingDiv.className = "relative z-10 max-w-[85%] self-start bg-white dark:bg-[#202c33] px-4 py-3 rounded-2xl rounded-tl-none shadow-sm flex items-center gap-1 shrink-0 border border-gray-100 dark:border-zinc-800/80";
                    typingDiv.innerHTML = `
                        <span class="w-1.5 h-1.5 bg-zinc-500 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
                        <span class="w-1.5 h-1.5 bg-zinc-500 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
                        <span class="w-1.5 h-1.5 bg-zinc-500 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
                    `;
                    chatBody.appendChild(typingDiv);
                    chatBody.scrollTop = chatBody.scrollHeight;
                    
                    const startTime = Date.now();
                    
                    try {
                        const k1 = "Bearer sk-or-v1-";
                        const k2 = "6aae9b1ad8404d1585f166de82ec6dbd3feed768aeec21c1a0da536a562f311b";
                        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "Authorization": k1 + k2,
                                "HTTP-Referer": "https://consultor-ia.com.co",
                                "X-Title": "Consultor IA Landing Demo"
                            },
                            body: JSON.stringify({
                                model: "meta-llama/llama-3.1-8b-instruct",
                                messages: chatHistory,
                                temperature: 0.7
                            })
                        });
                        
                        if (!response.ok) {
                            const errText = await response.text();
                            console.error("OpenRouter Error Detail:", response.status, errText);
                            throw new Error("Respuesta de API incorrecta: " + response.status);
                        }
                        
                        const data = await response.json();
                        let botResponse = data.choices[0].message.content;
                        
                        // Esperar al menos 3 segundos en total para simular el tipeado real
                        const elapsed = Date.now() - startTime;
                        if (elapsed < 3000) {
                            await new Promise(resolve => setTimeout(resolve, 3000 - elapsed));
                        }
                        
                        // Remover la burbuja de escribiendo
                        typingDiv.remove();
                        
                        // Parsear de forma ultra robusta y tolerante el tag de confirmación
                        const confirmIdx = botResponse.indexOf("[CONFIRMAR_CITA:");
                        if (confirmIdx !== -1) {
                            const endIdx = botResponse.indexOf("]", confirmIdx);
                            if (endIdx !== -1) {
                                const fullTag = botResponse.substring(confirmIdx, endIdx + 1);
                                const tagContent = botResponse.substring(confirmIdx + 16, endIdx).trim();
                                const parts = tagContent.split("|").map(p => p.trim());
                                
                                // Extraer fecha y hora de la primera parte
                                const dateTimePart = parts[0];
                                const dateMatch = dateTimePart.match(/(\d{4}-\d{2}-\d{2})/);
                                const timeMatch = dateTimePart.match(/(\d{2}:\d{2})/);
                                
                                if (dateMatch && timeMatch) {
                                    const dateKey = dateMatch[1];
                                    const timeKey = timeMatch[1];
                                    
                                    // Nombre es la segunda parte o fallback
                                    let clientName = "Usuario Demo";
                                    if (parts.length > 1 && parts[1]) {
                                        clientName = parts[1];
                                    }
                                    
                                    // Email es la tercera parte o fallback
                                    let clientEmail = "demo@consultor-ia.com.co";
                                    if (parts.length > 2 && parts[2]) {
                                        clientEmail = parts[2];
                                    } else if (parts.length > 1 && parts[1].includes("@")) {
                                        clientEmail = parts[1];
                                        clientName = "Usuario Demo";
                                    }
                                    
                                    // Validar que el email sea provisto por el usuario y sea válido
                                    const isEmailValid = clientEmail && clientEmail.includes("@") && !clientEmail.toUpperCase().includes("EMAIL") && !clientEmail.includes("example.com") && clientEmail.includes(".");
                                    
                                    if (isEmailValid) {
                                        // Guardar reserva en la base de datos local
                                        confirmedBooking = { date: dateKey, time: timeKey, name: clientName, email: clientEmail };
                                        if (!availabilityDb[dateKey]) {
                                            availabilityDb[dateKey] = {};
                                        }
                                        availabilityDb[dateKey][timeKey] = 'booked';
                                        
                                        // Remover la firma estructurada de la respuesta del bot para que no la vea el usuario
                                        botResponse = botResponse.substring(0, confirmIdx).trim() + " " + botResponse.substring(endIdx + 1).trim();
                                        botResponse = botResponse.trim();
                                        
                                        // Mostrar alerta premium superior de reserva
                                        bookingAlertText.textContent = "El Agente agendó tu cita para el " + formatHumanDate(dateKey) + " a las " + timeKey + ".";
                                        bookingSuccessAlert.classList.remove("opacity-0", "pointer-events-none", "-translate-y-4");
                                        bookingSuccessAlert.classList.add("opacity-100", "translate-y-0");
                                        
                                        // Actualizar los datos del Ticket lateral derecho
                                        document.getElementById("ticket-name").textContent = clientName;
                                        document.getElementById("ticket-email").textContent = clientEmail;
                                        document.getElementById("ticket-date").textContent = formatHumanDate(dateKey);
                                        document.getElementById("ticket-time").textContent = timeKey;
                                        
                                        // Activar visualización del ticket y checkmark animado en el panel derecho
                                        const emptyState = document.getElementById("booking-status-empty");
                                        const successState = document.getElementById("booking-status-success");
                                        const checkmark = document.getElementById("success-checkmark");
                                        const statusCard = document.getElementById("booking-status-card");
                                        
                                        emptyState.classList.add("hidden");
                                        successState.classList.remove("hidden");
                                        successState.classList.add("flex");
                                        
                                        statusCard.className = "w-full h-auto min-h-[200px] lg:flex-1 flex flex-col items-center justify-center text-center p-4 rounded-3xl bg-gradient-to-br from-emerald-50/40 to-teal-50/30 dark:from-emerald-950/35 dark:to-teal-950/20 border border-emerald-100 dark:border-emerald-800/40 shadow-inner transition-all duration-500 overflow-hidden relative";
                                        
                                        // Ocultar calendario y mostrar ticket en versión móvil para maximizar espacio
                                        const leftCol = document.getElementById("calendar-left-col");
                                        const rightCol = document.getElementById("calendar-right-col");
                                        if (leftCol && rightCol) {
                                            leftCol.classList.add("hidden-mobile");
                                            rightCol.classList.remove("hidden-mobile");
                                            rightCol.classList.add("visible-mobile-flex");
                                        }
                                        
                                        setTimeout(() => {
                                            checkmark.classList.remove("scale-0");
                                            checkmark.classList.add("scale-100");
                                        }, 100);
                                        
                                        // Actualizar calendario visualmente
                                        renderCalendar(currentYear, currentMonth);
                                        if (selectedDateStr === dateKey) {
                                            const dummyDate = new Date(dateKey + "T00:00:00");
                                            selectDate(dateKey, dummyDate);
                                        }
                                    } else {
                                        // Si el email no es válido, remover el tag para que no se vea feo pero NO confirmar la cita
                                        botResponse = botResponse.substring(0, confirmIdx).trim() + " " + botResponse.substring(endIdx + 1).trim();
                                        botResponse = botResponse.trim();
                                    }
                                    
                                    // Ocultar alerta superior a los 7 segundos
                                    setTimeout(() => {
                                        bookingSuccessAlert.classList.add("opacity-0", "pointer-events-none", "-translate-y-4");
                                        bookingSuccessAlert.classList.remove("opacity-100", "translate-y-0");
                                    }, 7000);
                                }
                            }
                        }
                        
                        // Mostrar respuesta del bot
                        appendMessage('bot', botResponse);
                        chatHistory.push({"role": "assistant", "content": botResponse});
                        
                    } catch (error) {
                        console.error("Error:", error);
                        if (typingDiv) typingDiv.remove();
                        appendMessage('bot', "Lo siento, tuve un problema al procesar su solicitud. ¿Podría intentarlo de nuevo?");
                    } finally {
                        chatStatus.textContent = "en línea";
                        chatStatus.className = "text-white/80 text-xs mt-0.5";
                    }
                }
                
                // Respuestas rápidas (Quick Replies)
                const quickRepliesContainer = document.getElementById("chat-quick-replies");
                const btnQuickReply1 = document.getElementById("btn-quick-reply-1");
                const btnQuickReply2 = document.getElementById("btn-quick-reply-2");
                
                function handleQuickReply(text) {
                    if (quickRepliesContainer) {
                        quickRepliesContainer.style.display = "none";
                    }
                    chatInput.value = text;
                    sendMessage();
                }
                
                if (btnQuickReply1) {
                    btnQuickReply1.addEventListener("click", () => handleQuickReply("Hola"));
                }
                if (btnQuickReply2) {
                    btnQuickReply2.addEventListener("click", () => handleQuickReply("Me gustaría agendar una cita"));
                }

                // Vincular eventos del chat
                chatSendBtn.addEventListener("click", sendMessage);
                chatInput.addEventListener("keypress", function(e) {
                    if (e.key === "Enter") {
                        sendMessage();
                    }
                });
                
                // --- Inicialización Ejecutable ---
                initAvailabilityDb();
                selectedDateStr = formatDateKey(dateBase);
                selectDate(selectedDateStr, dateBase);
                renderCalendar(currentYear, currentMonth);
            });
        </script>
    </section>
    '''
    
    # Reemplazos dinámicos explícitos
    html = html.replace('__CIUDAD__', ciudad)
    html = html.replace('__INDUSTRIA__', industria)
    html = html.replace('__INDUSTRIA_SINGULAR__', industria_singular)
    html = html.replace('__CLIENTE_NEGOCIO__', cliente_negocio)
    html = html.replace('__BOT_INITIAL_MSG__', bot_initial_msg)
    import base64
    system_prompt_b64 = base64.b64encode(system_prompt.encode('utf-8')).decode('utf-8')
    html = html.replace('__SYSTEM_PROMPT_B64__', system_prompt_b64)
    
    return html




def build_roadmap_html(row):
    ciudad = row.get('Ciudad', '')
    industria = row.get('Industria', 'tu negocio')
    
    html = f'''
    <section id="como-funciona" class="py-24 bg-[#FDFBF7] dark:bg-zinc-900">
        <div class="container mx-auto px-4 max-w-5xl">
            <div class="text-center mb-16">
                <span class="text-brand dark:text-brand-light font-normal tracking-wider uppercase text-sm mb-2 block">Implementación Rápida</span>
                <h2 class="text-3xl md:text-5xl font-header font-bold mb-6">Roadmap para {industria} en {ciudad}</h2>
                <p class="text-xl text-zinc-600 dark:text-zinc-400">Lanzamos tu agente de IA en 4 pasos simples, sin que tengas que programar nada.</p>
            </div>
            
            <div class="relative">
                <!-- Línea conectora -->
                <div class="absolute left-6 md:left-1/2 top-0 bottom-0 w-px bg-accent/30 dark:bg-accent/20 -translate-x-1/2"></div>
                
                <div class="space-y-12">
                    <!-- Paso 1 -->
                    <div class="relative flex flex-col md:flex-row items-start md:items-center md:justify-between group">
                        <div class="md:w-5/12 text-left md:text-right pl-16 md:pl-0 md:pr-12">
                            <h3 class="text-2xl font-header font-bold mb-3 text-gray-1 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light transition-colors">1. Auditoría y Estrategia</h3>
                            <p class="text-gray-500 dark:text-slate-400">Analizamos el flujo de ventas de tu {industria} y definimos la personalidad y base de conocimiento del agente.</p>
                        </div>
                        <div class="absolute top-0 left-0 md:left-1/2 md:-translate-y-1/2 -translate-x-0 md:-translate-x-1/2 w-12 h-12 rounded-full bg-[#FDFBF7] dark:bg-zinc-900 border-4 border-brand dark:border-white/20 flex items-center justify-center font-bold text-brand dark:text-brand-light dark:text-white shadow-xl z-10">1</div>
                        <div class="md:w-5/12 pl-0 md:pl-12 hidden md:block"></div>
                    </div>
                    
                    <!-- Paso 2 -->
                    <div class="relative flex flex-col md:flex-row items-start md:items-center md:justify-between group">
                        <div class="md:w-5/12 pr-0 md:pr-12 hidden md:block"></div>
                        <div class="absolute top-0 left-0 md:left-1/2 md:-translate-y-1/2 -translate-x-0 md:-translate-x-1/2 w-12 h-12 rounded-full bg-[#FDFBF7] dark:bg-zinc-900 border-4 border-brand dark:border-white/20 flex items-center justify-center font-bold text-brand dark:text-brand-light dark:text-white shadow-xl z-10">2</div>
                        <div class="md:w-5/12 pl-16 md:pl-12 text-left">
                            <h3 class="text-2xl font-header font-bold mb-3 text-gray-1 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light transition-colors">2. Entrenamiento IA</h3>
                            <p class="text-gray-500 dark:text-slate-400">Cargamos tus PDFs, FAQs e historial de WhatsApp para que la IA responda como tu mejor vendedor.</p>
                        </div>
                    </div>
                    
                    <!-- Paso 3 -->
                    <div class="relative flex flex-col md:flex-row items-start md:items-center md:justify-between group">
                        <div class="md:w-5/12 text-left md:text-right pl-16 md:pl-0 md:pr-12">
                            <h3 class="text-2xl font-header font-bold mb-3 text-gray-1 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light transition-colors">3. Integración WhatsApp</h3>
                            <p class="text-gray-500 dark:text-slate-400">Conectamos el cerebro de IA con el número de WhatsApp oficial de tu negocio de forma segura.</p>
                        </div>
                        <div class="absolute top-0 left-0 md:left-1/2 md:-translate-y-1/2 -translate-x-0 md:-translate-x-1/2 w-12 h-12 rounded-full bg-[#FDFBF7] dark:bg-zinc-900 border-4 border-brand dark:border-white/20 flex items-center justify-center font-bold text-brand dark:text-brand-light dark:text-white shadow-xl z-10">3</div>
                        <div class="md:w-5/12 pl-0 md:pl-12 hidden md:block"></div>
                    </div>
                    
                    <!-- Paso 4 -->
                    <div class="relative flex flex-col md:flex-row items-start md:items-center md:justify-between group">
                        <div class="md:w-5/12 pr-0 md:pr-12 hidden md:block"></div>
                        <div class="absolute top-0 left-0 md:left-1/2 md:-translate-y-1/2 -translate-x-0 md:-translate-x-1/2 w-12 h-12 rounded-full bg-brand dark:bg-zinc-800 border-4 border-brand dark:border-white/20 flex items-center justify-center font-bold text-white shadow-xl z-10">4</div>
                        <div class="md:w-5/12 pl-16 md:pl-12 text-left">
                            <h3 class="text-2xl font-header font-bold mb-3 text-gray-1 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light transition-colors">4. Lanzamiento y Optimización</h3>
                            <p class="text-gray-500 dark:text-slate-400">Encendemos el agente. Monitoreamos las primeras conversaciones y ajustamos sus respuestas en tiempo real.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    '''
    return html

def build_roi_table_html(row):
    moneda = row.get('Moneda', 'USD')
    precio_bajo = row.get('Precio_Bajo', '100')
    
    try:
        precio_num = float(re.sub(r'[^\d.]', '', str(precio_bajo)))
        
        # Las exportaciones a veces truncan los miles (ej: 800.0 para COP en vez de 800.000)
        # Para todas las monedas excepto USD, multiplicamos por 1000 si parece estar truncado
        # (Todos los CSV analizados para moneda != USD estaban divididos por 1000 en Precio_Bajo)
        if moneda != 'USD':
            precio_num *= 1000
            
        costo_humano_num = precio_num * 4
        costo_humano = f"{moneda} {costo_humano_num:,.0f}"
        precio_bajo_str = f"{moneda} {precio_num:,.0f}"
    except:
        costo_humano = f"{moneda} 400"
        precio_bajo_str = f"{moneda} 100"
        
    html = f'''
    <section class="py-16 bg-[#FDFBF7] dark:bg-zinc-900 border-y border-gray-border dark:border-zinc-800">
        <div class="container mx-auto px-4 max-w-4xl">
            <div class="text-center mb-10">
                <h2 class="text-3xl font-header font-bold mb-4">Humano vs. Agente IA</h2>
                <p class="text-lg text-gray-500 dark:text-slate-400">¿Por qué un Agente es la decisión más inteligente para tu ROI?</p>
            </div>
            
            <div class="overflow-x-auto rounded-2xl shadow-xl">
                <table class="w-full text-left bg-white dark:bg-zinc-900 border-collapse min-w-[600px]">
                    <thead>
                        <tr class="bg-gray-100 dark:bg-zinc-800 border-b border-gray-border dark:border-zinc-700">
                            <th class="p-6 font-bold text-gray-700 dark:text-slate-300 w-1/3">Característica</th>
                            <th class="p-6 font-bold text-gray-500 dark:text-slate-400 w-1/3 text-center border-x border-gray-border dark:border-zinc-700">Empleado Tradicional</th>
                            <th class="p-6 font-bold text-brand dark:text-brand-light w-1/3 text-center bg-brand/5 dark:bg-brand/10">Agente IA Consultor</th>
                        </tr>
                    </thead>
                    <tbody class="text-gray-600 dark:text-slate-400">
                        <tr class="border-b border-gray-border dark:border-zinc-800 hover:bg-slate-50 dark:hover:bg-zinc-900/50 transition-colors">
                            <td class="p-5 font-medium text-gray-800 dark:text-slate-200">Disponibilidad</td>
                            <td class="p-5 text-center">8 horas / Lunes a Viernes</td>
                            <td class="p-5 text-center font-bold text-brand dark:text-brand-light bg-brand/5 dark:bg-brand/10">24/7/365 (Sin descansos)</td>
                        </tr>
                        <tr class="border-b border-gray-border dark:border-zinc-800 hover:bg-slate-50 dark:hover:bg-zinc-900/50 transition-colors">
                            <td class="p-5 font-medium text-gray-800 dark:text-slate-200">Velocidad de Respuesta</td>
                            <td class="p-5 text-center">15 min - 2 horas</td>
                            <td class="p-5 text-center font-bold text-brand dark:text-brand-light bg-brand/5 dark:bg-brand/10">&lt; 3 Segundos</td>
                        </tr>
                        <tr class="border-b border-gray-border dark:border-zinc-800 hover:bg-slate-50 dark:hover:bg-zinc-900/50 transition-colors">
                            <td class="p-5 font-medium text-gray-800 dark:text-slate-200">Capacidad Simultánea</td>
                            <td class="p-5 text-center">1 cliente a la vez</td>
                            <td class="p-5 text-center font-bold text-brand dark:text-brand-light bg-brand/5 dark:bg-brand/10">Ilimitada</td>
                        </tr>
                        <tr class="hover:bg-slate-50 dark:hover:bg-zinc-900/50 transition-colors">
                            <td class="p-5 font-medium text-gray-800 dark:text-slate-200">Costo Mensual Estimado</td>
                            <td class="p-5 text-center text-red-500 font-medium">Aprox. {costo_humano}</td>
                            <td class="p-5 text-center font-bold text-brand dark:text-brand-light bg-brand/5 dark:bg-brand/10">Desde {precio_bajo_str}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>
    '''
    return html


def build_calculadora_html(row):
    moneda = row.get('Moneda', 'USD')
    industria = row.get('Industria', 'negocio')
    
    html = f'''
    <section class="py-16 bg-white dark:bg-zinc-950">
        <div class="container mx-auto px-4 max-w-4xl">
            <div class="text-center mb-10">
                <span class="text-brand dark:text-brand-light font-normal tracking-wider uppercase text-sm mb-2 block">Descubre tu Potencial</span>
                <h2 class="text-3xl font-header font-bold mb-4">Calculadora de ROI para {industria}</h2>
                <p class="text-lg text-gray-500 dark:text-slate-400">Estima cuánto dinero y tiempo estás dejando en la mesa por no automatizar.</p>
            </div>
            
            <div class="bg-[#FDFBF7] dark:bg-zinc-900/50 border border-gray-border dark:border-zinc-800 rounded-3xl p-8 shadow-2xl flex flex-col md:flex-row gap-12 backdrop-blur-sm">
                
                <!-- Controles -->
                <div class="w-full md:w-1/2 flex flex-col justify-center space-y-10">
                    <div>
                        <div class="flex justify-between mb-4">
                            <label class="font-header font-bold text-gray-700 dark:text-zinc-200 text-lg">Chats diarios recibidos</label>
                            <span id="calc-chats-val" class="text-brand dark:text-white font-bold text-2xl">50</span>
                        </div>
                        <input type="range" id="calc-chats" min="10" max="500" value="50" class="w-full h-2 bg-zinc-200 dark:bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-brand dark:accent-white">
                        <p class="text-xs text-gray-400 dark:text-zinc-500 mt-3 font-medium uppercase tracking-wider">Mensajes de WhatsApp por día</p>
                    </div>
                    
                    <div>
                        <div class="flex justify-between mb-4">
                            <label class="font-header font-bold text-gray-700 dark:text-zinc-200 text-lg">Ticket promedio de venta</label>
                            <span id="calc-ticket-val" class="text-brand dark:text-white font-bold text-2xl">{moneda} 100</span>
                        </div>
                        <input type="range" id="calc-ticket" min="10" max="1000" step="10" value="100" class="w-full h-2 bg-zinc-200 dark:bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-brand dark:accent-white">
                        <p class="text-xs text-gray-400 dark:text-zinc-500 mt-3 font-medium uppercase tracking-wider">Valor promedio de lo que vendes</p>
                    </div>
                </div>
                
                <!-- Resultados -->
                <div class="w-full md:w-1/2 bg-white dark:bg-zinc-950/80 border border-gray-100 dark:border-zinc-800 rounded-2xl p-8 flex flex-col justify-center space-y-8 shadow-inner">
                    <div class="text-center">
                        <p class="text-sm text-gray-500 dark:text-zinc-400 mb-2 uppercase tracking-widest font-semibold">Horas ahorradas al mes</p>
                        <div class="text-5xl font-header font-extrabold text-zinc-900 dark:text-white" id="res-hours">125h</div>
                    </div>
                    
                    <div class="h-px bg-gradient-to-r from-transparent via-gray-200 dark:via-zinc-800 to-transparent w-full"></div>
                    
                    <div class="text-center">
                        <p class="text-sm text-gray-500 dark:text-zinc-400 mb-2 uppercase tracking-widest font-semibold">Leads recuperados (Est. 20%)</p>
                        <div class="text-4xl font-header font-extrabold text-zinc-900 dark:text-white" id="res-leads">+300</div>
                    </div>
                    
                    <div class="h-px bg-gradient-to-r from-transparent via-gray-200 dark:via-zinc-800 to-transparent w-full"></div>
                    
                    <div class="text-center bg-brand/5 dark:bg-white/5 rounded-2xl p-6 border border-brand/10 dark:border-white/10">
                        <p class="text-xs text-brand dark:text-brand-light dark:text-white font-bold mb-2 uppercase tracking-tighter">Ingresos Extra Estimados (Mes)</p>
                        <div class="text-4xl font-header font-extrabold text-brand dark:text-brand-light dark:text-white" id="res-revenue">{moneda} 4,500</div>
                        <p class="text-[10px] text-gray-400 dark:text-zinc-500 mt-4 leading-tight">*Basado en una tasa de cierre conservadora del 15%.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            document.addEventListener("DOMContentLoaded", function() {{
                const calcChats = document.getElementById('calc-chats');
                const calcTicket = document.getElementById('calc-ticket');
                const valChats = document.getElementById('calc-chats-val');
                const valTicket = document.getElementById('calc-ticket-val');
                
                const resHours = document.getElementById('res-hours');
                const resLeads = document.getElementById('res-leads');
                const resRevenue = document.getElementById('res-revenue');
                
                function updateCalculator() {{
                    if(!calcChats || !calcTicket) return;
                    const chats = parseInt(calcChats.value);
                    const ticket = parseInt(calcTicket.value);
                    
                    valChats.textContent = chats;
                    valTicket.textContent = '{moneda} ' + ticket.toLocaleString();
                    
                    const hoursSaved = Math.round((chats * 30 * 5) / 60);
                    resHours.textContent = hoursSaved.toLocaleString() + 'h';
                    
                    const leadsLostPerMonth = Math.round((chats * 30) * 0.20);
                    resLeads.textContent = "+" + leadsLostPerMonth.toLocaleString();
                    
                    const extraRevenue = Math.round(leadsLostPerMonth * 0.15 * ticket);
                    resRevenue.textContent = '{moneda} ' + extraRevenue.toLocaleString();
                }}
                
                calcChats.addEventListener('input', updateCalculator);
                calcTicket.addEventListener('input', updateCalculator);
                
                updateCalculator();
            }});
        </script>
    </section>
    '''
    return html


def build_footer_html(data):
    """Genera un footer premium con enlaces a industrias y ciudades principales."""
    
    # Obtener industrias únicas y sus URLs (primer encuentro)
    industries = {}
    for row in data:
        if row.get('Estado') != 'PUBLICAR': continue
        ind = row.get('Industria')
        if ind and ind not in industries:
            industries[ind] = row.get('URL_Final')
            
    # Obtener ciudades principales (agrupar por país, sin duplicados)
    countries = {}
    seen_cities = {}
    for row in data:
        if row.get('Estado') != 'PUBLICAR': continue
        pais = row.get('País')
        ciudad = row.get('Ciudad')
        url = row.get('URL_Final')
        if pais and ciudad and url:
            if pais not in countries:
                countries[pais] = []
                seen_cities[pais] = set()
            if ciudad not in seen_cities[pais] and len(countries[pais]) < 8:
                countries[pais].append((ciudad, url))
                seen_cities[pais].add(ciudad)

    # Construir HTML de industrias
    ind_links = ""
    for name, url in sorted(industries.items())[:10]:
        ind_links += f'<li><a href="/{url.strip("/")}/" class="hover:text-accent transition-colors">{name}</a></li>'

    # Construir HTML de ciudades
    geo_links = ""
    for pais, city_list in countries.items():
        geo_links += f'<div class="flex flex-col gap-2"><h4 class="font-bold text-zinc-900 dark:text-white text-xs uppercase tracking-widest mb-2">{pais}</h4><ul class="space-y-2">'
        for city, url in city_list:
            geo_links += f'<li><a href="/{url.strip("/")}/" class="hover:text-accent transition-colors">{city}</a></li>'
        geo_links += '</ul></div>'

    footer = f'''
<footer class="bg-[#FDFBF7] dark:bg-zinc-950 border-t border-gray-border dark:border-zinc-800 pt-20 pb-10">
    <div class="container mx-auto px-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">
            <!-- Col 1: Brand -->
            <div class="flex flex-col gap-6">
                <a href="/" class="flex items-center gap-2">
                    <span class="font-header font-extrabold tracking-tighter text-3xl text-zinc-900 dark:text-white">Consultor-<span class="text-brand dark:text-brand-light">IA</span></span>
                </a>
                <p class="text-zinc-600 dark:text-zinc-400 text-sm leading-relaxed">
                    Transformamos la atención al cliente en LATAM con Agentes de Inteligencia Artificial que trabajan 24/7 en WhatsApp.
                </p>
                <div class="flex gap-4">
                    <a href="https://wa.me/{{WA_NUMERO}}" class="w-10 h-10 rounded-full bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center text-zinc-600 dark:text-slate-400 hover:bg-accent hover:text-white transition-all"><i class="fab fa-whatsapp"></i></a>
                    <a href="#" class="w-10 h-10 rounded-full bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center text-zinc-600 dark:text-slate-400 hover:bg-accent hover:text-white transition-all"><i class="fab fa-linkedin-in"></i></a>
                    <a href="#" class="w-10 h-10 rounded-full bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center text-zinc-600 dark:text-slate-400 hover:bg-accent hover:text-white transition-all"><i class="fab fa-instagram"></i></a>
                </div>
            </div>

            <!-- Col 2: Industrias -->
            <div>
                <h4 class="font-header font-bold text-zinc-900 dark:text-white text-lg mb-6">Soluciones</h4>
                <ul class="space-y-3 text-sm text-zinc-600 dark:text-zinc-400">
                    {ind_links}
                </ul>
            </div>

            <!-- Col 3 & 4: Ciudades -->
            <div class="lg:col-span-2">
                <h4 class="font-header font-bold text-zinc-900 dark:text-white text-lg mb-6">Presencia en LATAM</h4>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-8 text-sm text-zinc-600 dark:text-zinc-400">
                    {geo_links}
                </div>
            </div>
        </div>

        <div class="pt-8 border-t border-gray-border dark:border-zinc-800 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-gray-400 dark:text-slate-500">
            <div class="flex gap-6">
                <span>© 2026 Consultor-IA. Todos los derechos reservados.</span>
                <a href="/sitemap.xml" class="hover:text-zinc-900 dark:hover:text-white transition-colors">Sitemap</a>
            </div>
            <div class="flex gap-4">
                <a href="/aviso-legal/" class="hover:text-zinc-900 dark:hover:text-white transition-colors">Aviso Legal</a>
                <a href="/politica-de-privacidad/" class="hover:text-zinc-900 dark:hover:text-white transition-colors">Política de Privacidad</a>
            </div>
        </div>
    </div>
</footer>
<!-- Script del Modal de WhatsApp (con cache buster) -->
<script src="/js/wa-modal.js?v=1.3" charset="utf-8" defer></script>
'''
    return footer.replace("{WA_NUMERO}", str(WA_NUMERO))
def build_home_page(data):
    footer_html = build_footer_html(data)
    """Genera homepage con el mismo design system de las landings."""
    industry_icons = {
        'Restaurantes': 'fa-utensils',
        'Inmobiliarias': 'fa-building',
        'Clinicas Dentales': 'fa-tooth',
        'Gimnasios': 'fa-dumbbell',
        'Academias y Cursos': 'fa-graduation-cap',
        'Hoteles y Hostales': 'fa-hotel',
        'Salones de Belleza': 'fa-scissors',
        'Spas y Centros Esteticos': 'fa-spa',
        'Veterinarias': 'fa-paw',
        'Talleres Automotrices': 'fa-car',
    }
    industry_first_url = {}
    for row in data:
        if row.get('Estado') != 'PUBLICAR':
            continue
        ind = row['Industria']
        if ind not in industry_first_url:
            industry_first_url[ind] = row['URL_Final']

    industries_html = ""
    for ind, url in industry_first_url.items():
        icon = industry_icons.get(ind, 'fa-robot')
        industries_html += f"""
        <a href="{url}" class="group relative flex flex-col items-center justify-center gap-4 p-8 rounded-3xl border border-gray-200 dark:border-zinc-800/80 bg-white dark:bg-zinc-900/50 backdrop-blur-sm hover:border-zinc-900 dark:hover:border-white dark:hover:border-white/50 transition-all duration-500 hover:-translate-y-1 text-center">
            <!-- Hover Glow -->
            <div class="absolute inset-0 rounded-[inherit] bg-zinc-50 dark:bg-zinc-800/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

            <div class="relative z-10 w-16 h-16 rounded-2xl bg-brand/5 dark:bg-white/5 border border-brand/10 dark:border-white/10 flex items-center justify-center group-hover:scale-110 group-hover:bg-brand/10 dark:group-hover:bg-white/10 transition-all duration-500 shadow-inner">
                <i class="fas {icon} text-2xl text-brand dark:text-brand-light dark:text-white group-hover:text-zinc-900 dark:group-hover:text-white transition-colors"></i>
            </div>

            <div class="relative z-10 flex flex-col items-center">
                <span class="text-sm font-bold text-zinc-900 dark:text-white tracking-wide">{ind}</span>
                <div class="h-0 opacity-0 group-hover:h-auto group-hover:opacity-100 group-hover:mt-2 transition-all duration-300 overflow-hidden flex items-center justify-center">
                    <span class="text-xs font-semibold text-accent flex items-center gap-1 uppercase tracking-wider">Explorar <i class="fas fa-arrow-right text-[10px]"></i></span>
                </div>
            </div>
        </a>"""

    steps_data = [
        ("fa-search", "1. Diagnóstico", "Analizamos tu negocio, flujos de atención y dónde estás perdiendo clientes."),
        ("fa-brain", "2. Entrenamiento IA", "Cargamos tu información para que la IA responda como tu mejor vendedor."),
        ("fa-rocket", "3. Lanzamiento", "Activamos el agente en tu WhatsApp oficial con monitoreo en tiempo real."),
    ]
    steps_html = ""
    for icon, title, desc in steps_data:
        steps_html += f"""
        <div class="bg-[#FDFBF7] dark:bg-zinc-900 border border-gray-border dark:border-zinc-800 rounded-3xl p-8 transition-all duration-300 group">
            <div class="w-14 h-14 bg-brand/10 dark:bg-white/10 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <i class="fas {icon} text-2xl text-brand dark:text-brand-light"></i>
            </div>
            <h3 class="font-header font-bold text-xl mb-3">{title}</h3>
            <p class="text-gray-500 dark:text-slate-400 text-sm leading-relaxed">{desc}</p>
        </div>"""

    stats_data = [("297+", "Landings Activas"), ("24/7", "Disponibilidad"), ("&lt;3s", "Respuesta"), ("10+", "Países LATAM")]
    stats_html = ""
    for val, label in stats_data:
        stats_html += f"""
        <div class="text-center p-6 rounded-3xl border border-gray-border dark:border-zinc-800 bg-[#FDFBF7] dark:bg-zinc-900">
            <div class="text-4xl font-header font-extrabold text-brand dark:text-brand-light mb-1">{val}</div>
            <div class="text-sm text-gray-500 dark:text-slate-400">{label}</div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" sizes="48x48" href="https://consultor-ia.com.co/favicon-48x48.png">
    <link rel="icon" type="image/x-icon" href="https://consultor-ia.com.co/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://consultor-ia.com.co/apple-touch-icon.png">
    <title>Consultor IA | Expertos en Automatización con Inteligencia Artificial</title>
    <meta name="description" content="Automatiza la atención al cliente, ventas y reservas con Agentes IA para WhatsApp 24/7. Para restaurantes, clínicas, hoteles y más en LATAM.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://consultor-ia.com.co/">
    <meta property="og:title" content="Consultor IA | Agentes IA para Negocios LATAM">
    <meta property="og:description" content="Automatiza la atención al cliente, ventas y reservas con Agentes IA para WhatsApp 24/7. Para restaurantes, clínicas, hoteles y más en LATAM.">
    <meta property="og:url" content="https://consultor-ia.com.co/">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="es_CO">
    <meta property="og:site_name" content="Consultor IA">
    <meta property="og:image" content="https://consultor-ia.com.co/images/og-home.webp">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Consultor IA | Agentes IA para Negocios LATAM">
    <meta name="twitter:description" content="Automatiza la atención al cliente, ventas y reservas con Agentes IA para WhatsApp 24/7.">
    <meta name="twitter:image" content="https://consultor-ia.com.co/images/og-home.webp">
    <!-- Schema: Organization -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Consultor IA",
      "url": "https://consultor-ia.com.co",
      "logo": "https://consultor-ia.com.co/favicon-32x32.png",
      "description": "Automatizamos la atención al cliente, ventas y operaciones con Agentes de Inteligencia Artificial para empresas en toda Latinoamérica.",
      "areaServed": "LATAM",
      "sameAs": [
        "https://www.instagram.com/consultor.ia",
        "https://www.linkedin.com/company/consultor-ia"
      ],
      "contactPoint": {{
        "@type": "ContactPoint",
        "contactType": "sales",
        "availableLanguage": "Spanish",
        "url": "https://wa.me/573151206985"
      }}
    }}
    </script>
    <!-- Schema: AggregateRating -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Product",
      "name": "Agente IA para WhatsApp",
      "description": "Agente de Inteligencia Artificial para automatizar atención al cliente, ventas y reservas por WhatsApp en negocios LATAM.",
      "brand": {{"@type": "Brand", "name": "Consultor IA"}},
      "aggregateRating": {{
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "bestRating": "5",
        "worstRating": "1",
        "ratingCount": "115"
      }}
    }}
    </script>
    <!-- Schema: WebSite (Site Name) -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "Consultor IA",
      "alternateName": "Consultor Inteligencia Artificial",
      "url": "https://consultor-ia.com.co/"
    }}
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        'brand': '#18181b',
                        'brand-light': '#f4f4f5',
                        'accent': '#2563eb',
                        'success': '#10b981',
                        'gray-2': '#52525b',
                        'gray-border': '#e4e4e7',
                    }},
                    fontFamily: {{
                        body: ['"Inter"', 'sans-serif'],
                        header: ['"Playfair Display"', 'serif'],
                    }},
                    borderRadius: {{ '3xl': '24px' }},
                    animation: {{ 'fade-in-up': 'fadeInUp 0.8s ease-out forwards' }},
                    keyframes: {{
                        fadeInUp: {{
                            '0%': {{ opacity: '0', transform: 'translateY(20px)' }},
                            '100%': {{ opacity: '1', transform: 'translateY(0)' }},
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <script>
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
            document.documentElement.classList.add('dark');
        }} else {{ document.documentElement.classList.remove('dark'); }}
    </script>
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        h1, h2, h3, h4 {{ font-family: 'Playfair Display', serif; }}
        .glass {{ background: rgba(253,251,247,0.85); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }}
        .dark .glass {{ background: rgba(24,24,27,0.88); }}
        html, body {{ overscroll-behavior: none; }}
        .chat-bot {{ animation: fadeInUp 0.7s ease 0.5s forwards; opacity: 0; }}
        @keyframes fadeInUp {{ from {{ opacity:0; transform:translateY(16px); }} to {{ opacity:1; transform:translateY(0); }} }}
        .typing-dot {{ animation: typingBounce 1.2s infinite; }}
        .typing-dot:nth-child(2) {{ animation-delay:.2s; }}
        .typing-dot:nth-child(3) {{ animation-delay:.4s; }}
        @keyframes typingBounce {{ 0%,80%,100% {{ transform:translateY(0); }} 40% {{ transform:translateY(-5px); }} }}
    
        /* Background Animated Blobs */
        @keyframes blob-move-1 {{
            0% {{ transform: translate(0, 0) scale(1) rotate(0deg); }}
            33% {{ transform: translate(15vw, -10vh) scale(1.2) rotate(15deg); }}
            66% {{ transform: translate(-10vw, 15vh) scale(0.8) rotate(-15deg); }}
            100% {{ transform: translate(0, 0) scale(1) rotate(0deg); }}
        }}
        @keyframes blob-move-2 {{
            0% {{ transform: translate(0, 0) scale(1) rotate(0deg); }}
            33% {{ transform: translate(-15vw, 15vh) scale(1.2) rotate(-15deg); }}
            66% {{ transform: translate(15vw, -10vh) scale(0.8) rotate(15deg); }}
            100% {{ transform: translate(0, 0) scale(1) rotate(0deg); }}
        }}
        .bg-blob-1 {{ animation: blob-move-1 12s infinite ease-in-out; }}
        .bg-blob-2 {{ animation: blob-move-2 15s infinite ease-in-out; }}

        /* Smooth Global Background Blobs */
        @keyframes global-blob-1 {{
            0% {{ transform: translate(0, 0) scale(1) rotate(0deg); }}
            33% {{ transform: translate(20vw, -15vh) scale(1.2) rotate(10deg); }}
            66% {{ transform: translate(-15vw, 20vh) scale(0.8) rotate(-10deg); }}
            100% {{ transform: translate(0, 0) scale(1) rotate(0deg); }}
        }}
        @keyframes global-blob-2 {{
            0% {{ transform: translate(0, 0) scale(1) rotate(0deg); }}
            33% {{ transform: translate(-20vw, 20vh) scale(1.3) rotate(-15deg); }}
            66% {{ transform: translate(20vw, -15vh) scale(0.7) rotate(15deg); }}
            100% {{ transform: translate(0, 0) scale(1) rotate(0deg); }}
        }}
        @keyframes global-blob-3 {{
            0% {{ transform: translate(0, 0) scale(1) rotate(0deg); }}
            50% {{ transform: translate(25vw, 25vh) scale(1.4) rotate(20deg); }}
            100% {{ transform: translate(0, 0) scale(1) rotate(0deg); }}
        }}
        .global-blob-1 {{ animation: global-blob-1 6s infinite alternate ease-in-out; }}
        .global-blob-2 {{ animation: global-blob-2 8s infinite alternate ease-in-out; }}
        .global-blob-3 {{ animation: global-blob-3 10s infinite alternate ease-in-out; }}
    </style>
</head>
<body class="bg-white dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 transition-colors duration-300">

<!-- Smooth Global Background Blobs -->
<div class="fixed top-0 left-0 right-0 bottom-0 overflow-hidden pointer-events-none" style="z-index: -1;">
    <div class="global-blob-1 absolute -top-[20%] -left-[10%] w-[60vw] h-[60vw] md:w-[40vw] md:h-[40vw] rounded-full bg-gradient-to-br from-[#10b981]/10 to-[#06b6d4]/10 dark:from-[#10b981]/15 dark:to-[#06b6d4]/15 blur-[100px] md:blur-[150px]"></div>
    <div class="global-blob-2 absolute top-[20%] -right-[10%] w-[70vw] h-[70vw] md:w-[50vw] md:h-[50vw] rounded-full bg-gradient-to-br from-[#8b5cf6]/10 to-[#ec4899]/10 dark:from-[#8b5cf6]/15 dark:to-[#ec4899]/15 blur-[100px] md:blur-[150px]"></div>
    <div class="global-blob-3 absolute -bottom-[20%] left-[20%] w-[60vw] h-[60vw] md:w-[45vw] md:h-[45vw] rounded-full bg-gradient-to-br from-[#3b82f6]/10 to-[#8b5cf6]/10 dark:from-[#3b82f6]/15 dark:to-[#8b5cf6]/15 blur-[100px] md:blur-[150px]"></div>
</div>





<!-- HEADER -->
<header class="fixed top-4 inset-x-0 z-[100] flex justify-center px-4 pointer-events-none">
    <div class="w-full max-w-7xl glass rounded-full border border-gray-200 dark:border-zinc-800/80 shadow-2xl pointer-events-auto flex justify-between items-center px-6 py-3">
        <a href="/" class="flex items-center gap-2">
            <span class="font-header font-extrabold tracking-tighter text-3xl text-zinc-900 dark:text-white">Consultor-<span class="text-brand dark:text-brand-light">IA</span></span>
        </a>
        <nav class="hidden md:flex space-x-8 items-center">
            <a href="#como-funciona" class="font-medium text-zinc-600 dark:text-zinc-600 hover:text-brand dark:hover:text-brand-light transition-colors">Como Funciona</a>
            <a href="#industrias" class="font-medium text-zinc-600 dark:text-zinc-600 hover:text-brand dark:hover:text-brand-light transition-colors">Industrias</a>
            <a href="/blog/" class="font-medium text-zinc-600 dark:text-zinc-600 hover:text-brand dark:hover:text-brand-light transition-colors">Blog</a>
            <button id="theme-toggle" class="text-gray-500 dark:text-slate-400 hover:text-brand dark:hover:text-brand-light focus:outline-none rounded-lg text-lg p-2.5 transition-colors">
                <i id="theme-toggle-dark-icon" class="fas fa-moon hidden"></i>
                <i id="theme-toggle-light-icon" class="fas fa-sun hidden"></i>
            </button>
            <a href="https://wa.me/{WA_NUMERO}?text=Hola%2C+quiero+una+demo+del+agente+IA" target="_blank" class="group relative inline-flex items-center justify-center border border-zinc-900 dark:border-white px-6 py-2 overflow-hidden transition-all duration-500">
                <span class="absolute inset-0 w-full h-full bg-zinc-900 dark:bg-white origin-bottom scale-y-0 transition-transform duration-500 ease-[cubic-bezier(0.7,0,0.3,1)] group-hover:scale-y-100"></span>
                <span class="relative z-10 flex items-center gap-2 font-body text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-900 dark:text-white group-hover:text-white dark:group-hover:text-zinc-900 transition-colors duration-500 delay-75">Demo <i class="fab fa-whatsapp text-sm"></i></span>
            </a>
        </nav>
        <button class="md:hidden text-zinc-900 dark:text-slate-200 text-2xl" id="mobile-menu-btn"><i class="fas fa-bars"></i></button>
    </div>
</header>

<!-- HERO -->
<section class="relative pt-32 pb-24 lg:pt-40 lg:pb-32 overflow-hidden flex items-center min-h-[90vh]">
    <div class="absolute top-20 right-20 w-72 h-72 bg-accent/5 rounded-full blur-3xl -z-10"></div>
    <div class="absolute bottom-10 left-10 w-48 h-48 bg-success/5 rounded-full blur-2xl -z-10"></div>
    <div class="container mx-auto px-4 relative z-10 animate-fade-in-up">
        <div class="flex flex-col lg:flex-row items-center gap-12">
            <div class="lg:w-3/5">
                <span class="inline-flex items-center bg-brand/10 dark:bg-white/10 text-brand dark:text-brand-light px-4 py-2 rounded-full text-sm font-normal mb-6 shadow-sm border border-brand/20">
                    <span class="w-2 h-2 rounded-full bg-brand dark:bg-brand-light mr-2 animate-pulse"></span>
                    Agentes IA activos en 10+ paises de LATAM
                </span>
                <h1 class="text-5xl lg:text-7xl font-header font-extrabold mb-6 leading-[1.1] tracking-tight">
                    Tu negocio,<br>
                    <span class="text-brand dark:text-brand-light">atendiendo 24/7</span><br>
                    sin pausas.
                </h1>
                <p class="text-xl text-zinc-600 dark:text-zinc-300 mb-10 leading-relaxed max-w-2xl">
                    Implementamos <strong>Agentes de Inteligencia Artificial</strong> en WhatsApp que responden, agendan y venden por ti. Sin contratar mas personal. Sin perder un solo cliente.
                </p>
                <div class="flex flex-col sm:flex-row gap-4 mb-12">
                    <a href="https://wa.me/{WA_NUMERO}?text=Hola%2C+quiero+una+demo+del+agente+IA" target="_blank" class="group relative inline-flex items-center justify-center border border-zinc-900 dark:border-white px-8 py-4 overflow-hidden transition-all duration-500">
                        <span class="absolute inset-0 w-full h-full bg-zinc-900 dark:bg-white origin-bottom scale-y-0 transition-transform duration-500 ease-[cubic-bezier(0.7,0,0.3,1)] group-hover:scale-y-100"></span>
                        <span class="relative z-10 flex items-center gap-3 font-body text-[11px] font-bold uppercase tracking-[0.2em] text-zinc-900 dark:text-white group-hover:text-white dark:group-hover:text-zinc-900 transition-colors duration-500 delay-75">Solicitar Demo Gratis <i class="fab fa-whatsapp text-[14px]"></i></span>
                    </a>
                    <a href="#industrias" class="bg-transparent text-gray-800 dark:text-white border border-gray-border dark:border-zinc-700 px-8 py-4 rounded-full font-medium hover:bg-gray-50 dark:hover:bg-zinc-800 transition-all flex items-center justify-center text-lg">Ver Industrias</a>
                </div>
                <div class="flex flex-wrap items-center gap-6 border-t border-gray-border dark:border-zinc-800 pt-6">
                    <div class="flex items-center gap-3">
                        <div class="flex items-center text-[#FFD700] text-xl"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></div>
                        <div class="text-sm"><p class="font-normal">4.9/5.0</p><p class="text-gray-500 dark:text-slate-400 text-xs">Negocios en LATAM</p></div>
                    </div>
                    <div class="h-8 w-px bg-gray-border dark:bg-zinc-800 hidden sm:block"></div>
                    <div class="flex gap-4">
                        <span class="flex items-center text-sm font-normal text-gray-600 dark:text-slate-400"><i class="fas fa-check-circle text-success mr-1.5"></i>Setup 5-7 Dias</span>
                        <span class="flex items-center text-sm font-normal text-gray-600 dark:text-slate-400"><i class="fas fa-check-circle text-success mr-1.5"></i>WhatsApp Oficial</span>
                    </div>
                </div>
            </div>
            <div class="lg:w-2/5 w-full">
                <div class="relative bg-[#efeae2] dark:bg-[#0b141a] border border-gray-200 dark:border-zinc-800 rounded-3xl overflow-hidden shadow-2xl hover:shadow-[0_20px_50px_-12px_rgba(79,70,229,0.2)] transition-all">
                    <div class="bg-[#00a884] dark:bg-[#202c33] p-4 flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center shrink-0"><i class="fas fa-robot text-xl text-[#00a884]"></i></div>
                        <div><h3 class="font-medium text-white text-base">Consultor-IA Bot</h3><p class="text-white/80 text-xs">en linea</p></div>
                    </div>
                    <div class="p-5 flex flex-col gap-3 min-h-[280px] relative">
                        <div class="absolute inset-0 opacity-30 bg-[url('https://i.pinimg.com/736x/8c/98/99/8c98994518b575bfd8c949e91d20548b.jpg')] bg-cover bg-center -z-10"></div>
                        <div class="self-end bg-[#d9fdd3] dark:bg-[#005c4b] text-gray-800 dark:text-[#e9edef] rounded-lg rounded-tr-none py-2 px-3 max-w-[85%] text-[15px] shadow-sm">
                            hola buenas! tienen cita para manana? es urgente
                        </div>
                        <div class="chat-bot self-start bg-white dark:bg-[#202c33] text-gray-800 dark:text-[#e9edef] rounded-lg rounded-tl-none py-2 px-3 max-w-[90%] text-[15px] shadow-sm">
                            Hola! Claro que si. Tengo un espacio manana a las 9am y otro a las 3pm. Cual te queda mejor? Te lo reservo de una vez
                        </div>
                        <div class="self-start w-full mt-2">
                            <div class="bg-white/90 dark:bg-[#202c33]/90 backdrop-blur-sm border border-gray-100 dark:border-zinc-800 rounded-xl p-4 flex justify-between shadow-sm">
                                <div><p class="text-xs text-gray-500 dark:text-[#8696a0]">ROI Promedio</p><p class="font-bold text-accent dark:text-[#53bdeb] text-lg">+315%</p></div>
                                <div class="text-right"><p class="text-xs text-gray-500 dark:text-[#8696a0]">Implementacion</p><p class="font-bold text-gray-800 dark:text-[#e9edef] text-lg">5-7 Dias</p></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Testimonials Marquee (Scroll Infinito de Reseñas) -->
{{TESTIMONIALS_HTML}}

<!-- STATS -->
<section class="py-12 border-y border-gray-border dark:border-zinc-800 bg-[#FDFBF7] dark:bg-zinc-900">
    <div class="container mx-auto px-4 max-w-5xl">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            {stats_html}
        </div>
    </div>
</section>

<!-- COMO FUNCIONA -->
<section id="como-funciona" class="py-24">
    <div class="container mx-auto px-4 max-w-6xl">
        <div class="text-center mb-16 max-w-3xl mx-auto">
            <span class="text-brand dark:text-brand-light font-normal tracking-wider uppercase text-sm mb-2 block">Proceso</span>
            <h2 class="text-3xl md:text-5xl font-header font-bold mb-6 leading-tight">Activo en 7 dias</h2>
            <p class="text-xl text-zinc-600 dark:text-zinc-400">Sin codigo, sin complicaciones. Nosotros hacemos todo el trabajo tecnico.</p>
        </div>
        <div class="grid md:grid-cols-3 gap-8">
            {steps_html}
        </div>
    </div>
</section>

<!-- INDUSTRIAS -->
<section id="industrias" class="py-24 bg-[#FDFBF7] dark:bg-zinc-900 border-y border-gray-border dark:border-zinc-800">
    <div class="container mx-auto px-4 max-w-6xl">
        <div class="text-center mb-16 max-w-3xl mx-auto">
            <span class="text-brand dark:text-brand-light font-normal tracking-wider uppercase text-sm mb-2 block">Especializacion</span>
            <h2 class="text-3xl md:text-5xl font-header font-bold mb-6 leading-tight">Soluciones por Industria</h2>
            <p class="text-xl text-zinc-600 dark:text-zinc-400">Cada agente es entrenado con el lenguaje y procesos especificos de tu sector.</p>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {industries_html}
        </div>
    </div>
</section>

<!-- CTA FINAL -->
<section class="py-32 relative overflow-hidden">
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-accent/5 rounded-full blur-3xl -z-10"></div>
    <div class="container mx-auto px-4 max-w-4xl text-center">
        <span class="text-brand dark:text-brand-light font-normal tracking-wider uppercase text-sm mb-4 block">Listo para empezar?</span>
        <h2 class="text-4xl md:text-6xl font-header font-bold mb-6">Nunca pierdas<br>un cliente mas</h2>
        <p class="text-xl text-zinc-600 dark:text-zinc-400 mb-10 max-w-2xl mx-auto">Unete a los negocios de LATAM que ya atienden, agendan y venden en piloto automatico.</p>
        <a href="https://wa.me/{WA_NUMERO}?text=Hola%2C+quiero+una+demo+del+agente+IA" target="_blank" class="group relative inline-flex items-center justify-center border border-zinc-900 dark:border-white px-10 py-5 overflow-hidden transition-all duration-500">
            <span class="absolute inset-0 w-full h-full bg-zinc-900 dark:bg-white origin-bottom scale-y-0 transition-transform duration-500 ease-[cubic-bezier(0.7,0,0.3,1)] group-hover:scale-y-100"></span>
            <span class="relative z-10 flex items-center gap-3 font-body text-sm font-bold uppercase tracking-[0.2em] text-zinc-900 dark:text-white group-hover:text-white dark:group-hover:text-zinc-900 transition-colors duration-500 delay-75"><i class="fab fa-whatsapp text-lg"></i> Hablar con un Asesor</span>
        </a>
        <p class="text-gray-400 dark:text-slate-500 text-sm mt-6">Sin compromisos - Demo gratuita - Respuesta en menos de 1 hora</p>
    </div>
</section>

{footer_html}

<!-- Mobile Menu Overlay -->
<div id="mobile-menu" class="fixed inset-0 z-[110] bg-white/95 dark:bg-zinc-950/95 backdrop-blur-xl translate-x-full transition-transform duration-500 ease-in-out md:hidden">
    <div class="flex flex-col h-full p-8">
        <div class="flex justify-between items-center mb-12">
            <span class="font-header font-extrabold text-2xl text-zinc-900 dark:text-white">Consultor-<span class="text-brand dark:text-brand-light">IA</span></span>
            <div class="flex items-center gap-4">
                <button id="theme-toggle-mobile" class="text-gray-500 dark:text-slate-400 hover:text-brand dark:hover:text-brand-light focus:outline-none rounded-lg text-2xl p-2 transition-colors">
                    <i id="theme-toggle-dark-icon-mobile" class="fas fa-moon hidden"></i>
                    <i id="theme-toggle-light-icon-mobile" class="fas fa-sun hidden"></i>
                </button>
                <button id="close-menu-btn" class="text-3xl text-zinc-900 dark:text-white focus:outline-none">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
        
        <nav class="flex flex-col space-y-6 text-2xl font-header font-bold">
            <a href="/" class="hover:text-brand dark:hover:text-brand-light transition-colors">Inicio</a>
            <a href="#como-funciona" class="mobile-link hover:text-brand dark:hover:text-brand-light transition-colors">Cómo Funciona</a>
            <a href="#precios" class="mobile-link hover:text-brand dark:hover:text-brand-light transition-colors">Precios</a>
            <a href="/blog/" class="hover:text-brand dark:hover:text-brand-light transition-colors">Blog</a>
        </nav>

        <div class="mt-auto pt-8 border-t border-zinc-200 dark:border-zinc-800">
            <a href="https://wa.me/{WA_NUMERO}?text=Hola%2C+quiero+una+demo+del+agente+IA" target="_blank" class="flex items-center justify-center gap-3 bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 py-4 rounded-xl font-bold uppercase tracking-widest text-sm shadow-xl">
                Asesoría WhatsApp <i class="fab fa-whatsapp text-lg"></i>
            </a>
        </div>
    </div>
</div>

<script>
    var themeToggleBtn = document.getElementById('theme-toggle');
    var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
    
    var themeToggleBtnMobile = document.getElementById('theme-toggle-mobile');
    var themeToggleDarkIconMobile = document.getElementById('theme-toggle-dark-icon-mobile');
    var themeToggleLightIconMobile = document.getElementById('theme-toggle-light-icon-mobile');

    if (document.documentElement.classList.contains('dark')) {{ 
        themeToggleLightIcon.classList.remove('hidden'); 
        if(themeToggleLightIconMobile) themeToggleLightIconMobile.classList.remove('hidden');
    }} else {{ 
        themeToggleDarkIcon.classList.remove('hidden'); 
        if(themeToggleDarkIconMobile) themeToggleDarkIconMobile.classList.remove('hidden');
    }}

    const toggleThemeLogic = () => {{
        themeToggleDarkIcon.classList.toggle('hidden');
        themeToggleLightIcon.classList.toggle('hidden');
        if(themeToggleDarkIconMobile) themeToggleDarkIconMobile.classList.toggle('hidden');
        if(themeToggleLightIconMobile) themeToggleLightIconMobile.classList.toggle('hidden');
        
        if (document.documentElement.classList.contains('dark')) {{
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }} else {{
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }}
    }};

    themeToggleBtn.addEventListener('click', toggleThemeLogic);
    if(themeToggleBtnMobile) themeToggleBtnMobile.addEventListener('click', toggleThemeLogic);

    // --- Mobile Menu Toggle ---
    const mobileMenu = document.getElementById('mobile-menu');
    const openMenuBtn = document.getElementById('mobile-menu-btn');
    const closeMenuBtn = document.getElementById('close-menu-btn');
    const mobileLinks = document.querySelectorAll('.mobile-link');

    const toggleMenu = () => {{
        mobileMenu.classList.toggle('translate-x-full');
        document.body.classList.toggle('overflow-hidden');
    }};

    if (openMenuBtn) openMenuBtn.addEventListener('click', toggleMenu);
    if (closeMenuBtn) closeMenuBtn.addEventListener('click', toggleMenu);

    mobileLinks.forEach(link => {{
        link.addEventListener('click', () => {{
            mobileMenu.classList.add('translate-x-full');
            document.body.classList.remove('overflow-hidden');
        }});
    }});
</script>
</body>
</html>"""

    html = html.replace('{WA_NUMERO}', WA_NUMERO)
    testimonials_html = build_testimonials_html({'Ciudad': 'Colombia', 'Industria_Singular': 'negocio', 'Industria': 'Negocios', 'Cliente_Negocio': '', 'Cliente_Barrio': '', 'Barrios': 'Bogotá | Medellín | Cali | Barranquilla | Bucaramanga | Cartagena'})
    html = html.replace('{TESTIMONIALS_HTML}', testimonials_html)

    output_path = os.path.join(DIST_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path

def build_legal_pages(data):
    footer_html = build_footer_html(data)

    pages = [
        {
            "slug": "aviso-legal",
            "title": "Aviso Legal | Consultor IA",
            "h1": "Aviso Legal",
            "content": """
            <p>En cumplimiento de la normativa vigente, <strong>Consultor IA</strong> pone a disposición de los usuarios la siguiente información legal sobre el uso del sitio web <a href="https://consultor-ia.com.co" class="text-accent underline">consultor-ia.com.co</a>.</p>
            <h2 class="text-2xl font-header font-bold mt-10 mb-4">Titular del sitio web</h2>
            <p>Razón social: Consultor IA<br>Correo electrónico: contacto@consultor-ia.com.co<br>Sitio web: https://consultor-ia.com.co</p>
            <h2 class="text-2xl font-header font-bold mt-10 mb-4">Objeto y aceptación</h2>
            <p>El presente Aviso Legal regula el acceso y uso del sitio web de Consultor IA. El acceso y uso del sitio implica la aceptación plena de estas condiciones.</p>
            <h2 class="text-2xl font-header font-bold mt-10 mb-4">Propiedad intelectual</h2>
            <p>Todos los contenidos del sitio web (textos, imágenes, logotipos, código fuente) son propiedad de Consultor IA o de sus licenciantes y están protegidos por las leyes de propiedad intelectual. Queda prohibida su reproducción total o parcial sin autorización expresa.</p>
            <h2 class="text-2xl font-header font-bold mt-10 mb-4">Limitación de responsabilidad</h2>
            <p>Consultor IA no se responsabiliza de los daños y perjuicios que pudieran derivarse del uso del sitio web o de la imposibilidad de acceder al mismo. Nos reservamos el derecho de modificar o interrumpir el servicio sin previo aviso.</p>
            <h2 class="text-2xl font-header font-bold mt-10 mb-4">Legislación aplicable</h2>
            <p>Este aviso legal se rige por la legislación colombiana. Para cualquier controversia, las partes se someten a los tribunales competentes de Colombia.</p>
            """
        },
        {
            "slug": "politica-de-privacidad",
            "title": "Política de Privacidad | Consultor IA",
            "h1": "Política de Privacidad",
            "content": """
            <p>En <strong>Consultor IA</strong> nos tomamos muy en serio la privacidad de nuestros usuarios. Esta política describe cómo recopilamos, usamos y protegemos tu información personal.</p>
            <h2 class="text-2xl font-header font-bold mt-10 mb-4">Datos que recopilamos</h2>
            <p>Podemos recopilar los siguientes datos cuando interactúas con nuestro sitio o servicios:</p>
            <ul class="list-disc list-inside space-y-2 mt-4">
                <li>Nombre y datos de contacto (al solicitar información o demo)</li>
                <li>Número de teléfono (para contacto vía WhatsApp)</li>
                <li>Datos de navegación (mediante cookies y herramientas de analítica)</li>
                <li>Información sobre tu negocio (al contratar nuestros servicios)</li>
            </ul>
            <h2 class="text-2xl font-header font-bold mt-10 mb-4">Finalidad del tratamiento</h2>
            <p>Usamos tus datos para: responder solicitudes de información, proveer los servicios contratados, mejorar nuestros productos, y enviar comunicaciones comerciales relevantes (siempre con tu consentimiento).</p>
            <h2 class="text-2xl font-header font-bold mt-10 mb-4">Compartir datos con terceros</h2>
            <p>No vendemos ni alquilamos tus datos a terceros. Podemos compartirlos con proveedores de servicios (hosting, analítica, pagos) bajo acuerdos de confidencialidad y solo en la medida necesaria para prestar el servicio.</p>
            <h2 class="text-2xl font-header font-bold mt-10 mb-4">Tus derechos</h2>
            <p>Tienes derecho a acceder, rectificar, cancelar u oponerte al tratamiento de tus datos. Para ejercer estos derechos, contáctanos en: <a href="mailto:contacto@consultor-ia.com.co" class="text-accent underline">contacto@consultor-ia.com.co</a>.</p>
            <h2 class="text-2xl font-header font-bold mt-10 mb-4">Cookies</h2>
            <p>Nuestro sitio puede utilizar cookies propias y de terceros para mejorar la experiencia de navegación y realizar análisis estadísticos. Puedes configurar tu navegador para rechazar cookies, aunque esto puede afectar la funcionalidad del sitio.</p>
            <h2 class="text-2xl font-header font-bold mt-10 mb-4">Cambios en esta política</h2>
            <p>Nos reservamos el derecho de actualizar esta política en cualquier momento. La versión vigente siempre estará disponible en esta página.</p>
            <p class="mt-6 text-sm text-gray-400">Última actualización: mayo 2026</p>
            """
        }
    ]

    for page in pages:
        html = f"""<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" sizes="48x48" href="https://consultor-ia.com.co/favicon-48x48.png">
    <link rel="icon" type="image/x-icon" href="https://consultor-ia.com.co/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://consultor-ia.com.co/apple-touch-icon.png">
    <title>{page['title']}</title>
    <meta name="robots" content="noindex, follow">
    <link rel="canonical" href="https://consultor-ia.com.co/{page['slug']}/">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        'brand': '#18181b', 'brand-light': '#f4f4f5', 'accent': '#2563eb',
                        'success': '#10b981', 'gray-2': '#52525b', 'gray-border': '#e4e4e7',
                    }},
                    fontFamily: {{
                        body: ['"Inter"', 'sans-serif'], header: ['"Playfair Display"', 'serif'],
                    }}
                }}
            }}
        }}
    </script>
    <script>
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
            document.documentElement.classList.add('dark');
        }} else {{
            document.documentElement.classList.remove('dark');
        }}
    </script>
</head>
<body class="bg-white dark:bg-zinc-950 text-zinc-800 dark:text-zinc-200 font-body">

<!-- Smooth Global Background Blobs -->
<div class="fixed top-0 left-0 right-0 bottom-0 overflow-hidden pointer-events-none" style="z-index: -1;">
    <div class="global-blob-1 absolute -top-[20%] -left-[10%] w-[60vw] h-[60vw] md:w-[40vw] md:h-[40vw] rounded-full bg-gradient-to-br from-[#10b981]/10 to-[#06b6d4]/10 dark:from-[#10b981]/15 dark:to-[#06b6d4]/15 blur-[100px] md:blur-[150px]"></div>
    <div class="global-blob-2 absolute top-[20%] -right-[10%] w-[70vw] h-[70vw] md:w-[50vw] md:h-[50vw] rounded-full bg-gradient-to-br from-[#8b5cf6]/10 to-[#ec4899]/10 dark:from-[#8b5cf6]/15 dark:to-[#ec4899]/15 blur-[100px] md:blur-[150px]"></div>
    <div class="global-blob-3 absolute -bottom-[20%] left-[20%] w-[60vw] h-[60vw] md:w-[45vw] md:h-[45vw] rounded-full bg-gradient-to-br from-[#3b82f6]/10 to-[#8b5cf6]/10 dark:from-[#3b82f6]/15 dark:to-[#8b5cf6]/15 blur-[100px] md:blur-[150px]"></div>
</div>




    <header class="border-b border-gray-border dark:border-zinc-800 py-4 px-6">
        <div class="max-w-4xl mx-auto flex items-center justify-between">
            <a href="/" class="font-header font-extrabold tracking-tighter text-2xl text-zinc-900 dark:text-white">
                Consultor-<span class="text-brand dark:text-brand-light">IA</span>
            </a>
            <a href="/" class="text-sm text-gray-2 hover:text-zinc-900 dark:hover:text-white transition-colors">← Volver al inicio</a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-6 py-16">
        <h1 class="text-4xl md:text-5xl font-header font-bold mb-8">{page['h1']}</h1>
        <div class="prose max-w-none text-zinc-600 dark:text-zinc-400 leading-relaxed space-y-4">
            {page['content']}
        </div>
    </main>
    {footer_html}
</body>
</html>"""

        out_path = os.path.join(DIST_DIR, page['slug'], "index.html")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

def build_pillar_content(row):
    slug = row.get('Slug', '').strip('/')
    kw = row.get('Keyword_Principal', '')

    PILLAR_DATA = {
        'ia-para-negocios': {
            'intro': 'El 94% de los colombianos con internet usan WhatsApp. El 93% de los mexicanos también. No es una tendencia: es el canal de comunicación por defecto de toda LATAM, y ya mueve un mercado de comercio conversacional valorado en USD 18.200 millones, el 72% a través de WhatsApp. Tu negocio ya está en ese canal, te guste o no. La pregunta es si lo estás aprovechando o si cada mensaje sin responder se va donde la competencia.',
            'intro2': 'El problema no es atraer clientes a WhatsApp, eso ya pasa solo. El problema es que cada mensaje que llega exige atención inmediata, y la atención manual no escala. Un agente IA no reemplaza la relación con tus clientes: libera a tu equipo para que esa relación sea mejor.',
            'callout': '"El 80% de los clientes LATAM prefiere escribir por WhatsApp antes que llamar por teléfono. Si no respondes en 5 minutos, el siguiente en la lista sí lo hace."',
            'stats': [('94%', 'de colombianos con internet usan WhatsApp'), ('USD 18.2B', 'mercado conversacional LATAM en 2026'), ('98%', 'tasa de apertura en WhatsApp vs 22% del email'), ('3 seg', 'tiempo de respuesta del agente IA')],
            'benefits': [('fa-bolt', 'Respuesta inmediata 24/7', 'Ningún cliente espera más de 3 segundos. El agente responde preguntas, cotiza y agenda en tiempo real, incluso a las 3am.'), ('fa-chart-line', 'Más ventas, menos costo', 'Negocios con agente IA reportan entre 25% y 40% más conversiones al eliminar la fricción en el primer contacto.'), ('fa-brain', 'Aprende de tu negocio', 'El agente se entrena con tu menú, catálogo, precios y políticas. Responde como tu mejor vendedor, no como un bot genérico.')],
            'steps': [('Diagnóstico', 'Analizamos tus flujos de atención actuales e identificamos dónde se pierden clientes.'), ('Entrenamiento', 'Cargamos tu información: precios, productos, políticas y tono de marca.'), ('Lanzamiento', 'Activamos el agente en tu WhatsApp Business en menos de 72 horas.')],
            'faqs': [('¿Cuánto cuesta implementar IA en un negocio en LATAM?', 'Los planes empiezan desde USD 79/mes dependiendo del país y el volumen de conversaciones. Incluye configuración, entrenamiento y soporte.'), ('¿Necesito conocimientos técnicos?', 'No. Nosotros nos encargamos de todo: configuración, entrenamiento e integración con tu WhatsApp Business. Tú solo apruebas el contenido.'), ('¿En cuánto tiempo veo resultados?', 'La mayoría de negocios nota mejoras en la tasa de respuesta desde el primer día. Las métricas de conversión mejoran en las primeras 2-4 semanas.'), ('¿Funciona para cualquier tipo de negocio?', 'Sí. Tenemos experiencia en restaurantes, clínicas, hoteles, inmobiliarias, salones de belleza, gimnasios, talleres y más.')],
        },
        'consultor-inteligencia-artificial': {
            'intro': 'Hay dos tipos de consultores de IA: los que presentan decks durante tres meses y los que tienen un agente funcionando en tu WhatsApp en diez días. La diferencia no es tecnológica, es de mentalidad. En Consultor IA construimos e implementamos, no solo asesoramos. Cuando termina el proyecto, tú tienes el sistema operando, no un informe de 80 páginas.',
            'intro2': 'Trabajamos con empresas de todos los tamaños en Colombia, México, Argentina, Chile, Perú y otros seis países de LATAM. El criterio de entrada no es el tamaño del presupuesto: es si tienes un problema real de atención al cliente o ventas que la IA puede resolver. Si en la primera llamada no vemos ese problema, te lo decimos antes de cobrar un peso.',
            'callout': 'Señal de alerta con cualquier consultora: si no pueden mostrarte un agente funcionando en vivo en la primera reunión, probablemente no tienen implementaciones reales, solo presentaciones.',
            'stats': [('10+', 'industrias con implementaciones activas'), ('5-10 días', 'de kick-off a agente en producción'), ('9 países', 'en LATAM con clientes activos'), ('14 días', 'garantía de devolución sin condiciones')],
            'benefits': [('fa-user-tie', 'Estrategia personalizada', 'No hay soluciones genéricas. Analizamos tu modelo de negocio y diseñamos una hoja de ruta IA específica para tus objetivos.'), ('fa-tools', 'Implementación completa', 'No solo asesoramos: construimos, configuramos y entrenamos los agentes IA. Entregamos el sistema funcionando.'), ('fa-headset', 'Soporte continuo', 'Después del lanzamiento te acompañamos con monitoreo, ajustes y optimización mensual basada en datos reales.')],
            'steps': [('Auditoría', 'Revisamos tus procesos actuales de atención, ventas y operaciones para detectar dónde la IA genera más valor.'), ('Propuesta', 'Presentamos un plan de implementación con costos, tiempos y ROI esperado. Sin letra pequeña.'), ('Ejecución', 'Implementamos, entrenamos y lanzamos. En 5-10 días hábiles tu agente IA está operando.')],
            'faqs': [('¿Qué diferencia a Consultor IA de otras consultoras?', 'Nos especializamos exclusivamente en PYMES LATAM y en agentes conversacionales para WhatsApp. No vendemos proyectos enormes: vendemos resultados rápidos y medibles.'), ('¿Trabajan con empresas fuera de Colombia?', 'Sí. Tenemos clientes en México, Argentina, Chile, Perú, Ecuador, Panamá, Costa Rica, Uruguay y República Dominicana.'), ('¿Qué información necesito preparar?', 'Lista de preguntas frecuentes, catálogo de productos/servicios y tono de comunicación. Nosotros lo convertimos en el agente.'), ('¿Puedo ver una demo antes de contratar?', 'Sí. Agendamos una demo gratuita de 30 minutos donde muestras tu negocio en vivo y te mostramos cómo respondería el agente.')],
        },
        'ia-para-empresas': {
            'intro': 'Según datos de Microsoft para 2025, el 66% de las empresas colombianas ya usa inteligencia artificial en algún proceso. El 80% planea iniciar o escalar su transformación digital el próximo año. Si tu empresa todavía está evaluando si adoptar IA, no estás siendo cuidadoso: estás quedándote atrás. Los que llevan ventaja no empezaron con proyectos enormes, empezaron por un proceso concreto, midieron resultados y escalaron.',
            'intro2': 'El mayor riesgo en IA empresarial no es implementar demasiado rápido: es el "piloto purgatorio". Meses de comités, análisis y reuniones sin nada en producción. La estrategia que funciona es diferente: elegir el proceso con mayor volumen de fricciones repetitivas, lanzar en diez días, medir treinta días, y decidir con datos reales.',
            'callout': 'El 70% de las PYMES latinoamericanas planea seguir invirtiendo en IA. La diferencia entre las que prosperan y las que no no será si adoptan IA, sino cuándo empezaron.',
            'stats': [('66%', 'de empresas colombianas ya usa IA — Microsoft 2025'), ('80%', 'del volumen de consultas suele ser repetitivo'), ('60-90 días', 'para recuperar la inversión promedio'), ('24/7', 'operación continua sin costo adicional')],
            'benefits': [('fa-comments', 'Atención 24/7 sin contratar', 'Un agente IA maneja cientos de conversaciones simultáneas sin fatiga, errores ni días libres.'), ('fa-funnel-dollar', 'Pipeline de ventas automatizado', 'Califica leads, responde objeciones y agenda demos automáticamente mientras tu equipo se enfoca en cerrar.'), ('fa-sync', 'Integración con tus sistemas', 'Conectamos el agente con tu CRM, calendario, catálogo y sistema de pagos sin necesidad de cambiar tus herramientas.')],
            'steps': [('Mapeo de procesos', 'Identificamos los 3 procesos de mayor impacto para automatizar primero.'), ('Piloto rápido', 'Implementamos en 10 días y medimos resultados reales durante 30 días.'), ('Escala', 'Con los datos del piloto, expandimos a más procesos y canales.')],
            'faqs': [('¿Qué tamaño de empresa necesita IA?', 'Desde 5 empleados. Si tienes más de 20 conversaciones diarias por WhatsApp, ya necesitas automatización.'), ('¿Requiere integración con nuestro ERP?', 'Depende del caso. La mayoría de implementaciones funciona sin integración en la primera fase. Las integraciones se agregan después si hay necesidad.'), ('¿Cómo se mide el ROI?', 'Medimos tiempo de respuesta, tasa de conversión, leads calificados y horas de atención ahorradas. El promedio de nuestros clientes recupera la inversión en 60-90 días.'), ('¿La IA reemplaza a mi equipo?', 'No. La IA se encarga de las consultas repetitivas (70-80% del volumen). Tu equipo se enfoca en las conversaciones que realmente necesitan toque humano.')],
        },
        'ia-para-industria': {
            'intro': 'La IA no llega igual a todas las industrias. En una clínica dental, el problema principal son los no-shows. En una inmobiliaria, es el tiempo de respuesta a leads. En un restaurante, son las reservas que se pierden porque nadie contestó a las 9pm. En un hotel boutique, es responder en inglés y portugués sin tener un equipo multilingüe. Cada industria tiene su cuello de botella específico, y un agente IA bien configurado ataca exactamente ese punto.',
            'intro2': 'Lo que sí es común a todas las industrias LATAM: WhatsApp ya es el CRM informal de tu negocio, lo tengas o no reconocido. Los mensajes llegan, el equipo responde desde el celular personal, y no hay registro ni métricas. La IA empieza ordenando eso, y de ahí escala a lo que cada sector necesite.',
            'callout': 'Los mensajes de WhatsApp tienen una tasa de apertura del 98%. Los emails de marketing, 22%. Si tu industria aún apuesta todo al email, estás comunicándote en el canal que nadie lee.',
            'stats': [('98%', 'apertura en WhatsApp vs 22% del email'), ('35%+', 'crecimiento anual de WhatsApp Business en LATAM'), ('10+', 'industrias con implementaciones activas'), ('5M+', 'empresas medianas y grandes usan WhatsApp API en LATAM')],
            'benefits': [('fa-industry', 'Manufactura y logística', 'Automatiza pedidos, consultas de inventario y seguimiento de envíos. Reduce el 60% de llamadas entrantes al equipo de ventas.'), ('fa-shopping-cart', 'Retail y e-commerce', 'Asistentes de compra que recomiendan productos, responden sobre stock y recuperan carritos abandonados por WhatsApp.'), ('fa-heartbeat', 'Salud y bienestar', 'Agendamiento automático, recordatorios de citas, triaje básico y seguimiento post-consulta sin carga al personal.')],
            'steps': [('Evaluación sectorial', 'Analizamos las particularidades de tu industria y los casos de uso con mayor impacto.'), ('Configuración específica', 'El agente se entrena con el vocabulario, procesos y regulaciones de tu sector.'), ('Medición de KPIs', 'Definimos métricas específicas de la industria para evaluar el éxito.')],
            'faqs': [('¿Qué industrias atiende Consultor IA?', 'Restaurantes, hoteles, clínicas dentales, salones de belleza, spas, gimnasios, inmobiliarias, veterinarias y talleres automotrices, entre otros.'), ('¿La IA entiende terminología técnica de mi industria?', 'Sí. El agente se entrena con tu glosario, catálogo y procesos específicos. Responde con el vocabulario de tu sector.'), ('¿Puede manejar múltiples idiomas?', 'Sí. Especialmente útil para hoteles y turismo. El agente detecta el idioma del cliente y responde en el mismo.'), ('¿Funciona en sectores regulados como salud?', 'Sí, con los límites apropiados. El agente maneja agendamiento y consultas básicas pero escala al profesional cuando es necesario.')],
        },
        'automatizacion-con-ia': {
            'intro': 'Haz el ejercicio: anota los últimos 50 mensajes que recibiste por WhatsApp en tu negocio. Probablemente el 70-80% son variaciones de las mismas diez preguntas: horarios, precios, disponibilidad, formas de pago, dirección. Eso es lo que automatiza la IA primero, y es ahí donde está el mayor retorno. No en proyectos complejos de "transformación digital", sino en no tener que responder manualmente la misma pregunta por centésima vez.',
            'intro2': 'La automatización con IA no suena a menú telefónico ni a bot que dice "no entendí tu solicitud". Los agentes actuales entienden contexto, toleran errores de ortografía, procesan notas de voz y responden con el tono de tu marca. La diferencia que sienten los clientes no es "hablar con un bot" sino "respuesta instantánea a cualquier hora".',
            'callout': 'Automatizar el 80% de consultas repetitivas no significa ignorar el 20% restante. Significa que tu equipo puede dedicarle el 100% de su atención a las conversaciones que realmente valen.',
            'stats': [('80%', 'de consultas suelen ser 10 preguntas repetidas'), ('72h', 'para lanzar automatización básica activa'), ('40%', 'reducción de ausentismo con recordatorios automáticos'), ('<1 seg', 'tiempo de respuesta, a las 3am igual que a las 9am')],
            'benefits': [('fa-robot', 'Atención automatizada', 'Respuestas instantáneas a preguntas frecuentes, cotizaciones y agendamiento. Sin intervención humana para el 80% de los casos.'), ('fa-calendar-check', 'Agenda inteligente', 'El agente consulta disponibilidad real y confirma citas automáticamente. Cero llamadas para coordinar horarios.'), ('fa-bell', 'Recordatorios automáticos', 'Notifica a clientes sobre citas, pagos pendientes y promociones. Reduce ausentismo hasta un 40%.')],
            'steps': [('Identificar', 'Detectamos las 5 tareas más repetitivas de tu operación diaria.'), ('Automatizar', 'Configuramos flujos de automatización con IA para cada tarea identificada.'), ('Optimizar', 'Con los datos del primer mes, afinamos los flujos para maximizar conversiones.')],
            'faqs': [('¿Qué procesos se pueden automatizar con IA?', 'Atención al cliente, agendamiento, cotizaciones, seguimiento post-venta, recordatorios, calificación de leads y respuestas a preguntas frecuentes.'), ('¿La automatización suena robótica?', 'No. Nuestros agentes tienen conversaciones naturales: entienden contexto, jerga local y mensajes de voz.'), ('¿Se puede personalizar el tono?', 'Totalmente. El agente habla con el tono de tu marca: formal, cercano, técnico o desenfadado según definas.'), ('¿Qué pasa con consultas complejas?', 'El agente detecta cuándo una consulta supera su capacidad y escala al equipo humano con todo el contexto de la conversación.')],
        },
        'transformacion-digital-con-ia': {
            'intro': 'Según la encuesta de Microsoft para PyMEs de las Américas en 2025, el 77% de las empresas colombianas ya implementan o quieren implementar IA. Pero solo el 54% ha dado el primer paso. Ese 23% que quiere pero no ha empezado tiene un problema claro: saben que necesitan transformarse pero no saben por dónde. La respuesta casi siempre es la misma: por el proceso que más duele hoy, no por el que suena más tecnológico.',
            'intro2': 'La transformación digital que funciona no empieza con un proyecto de 6 meses. Empieza con un agente IA funcionando en WhatsApp en diez días, midiendo resultados reales durante 30 días, y escalando con los datos que ese primer mes entrega. Lo que no funciona: el "comité de transformación digital" que se reúne cada dos semanas sin nada en producción.',
            'callout': 'El 80% de las empresas colombianas planea iniciar su transformación digital este año. Las que empezaron hace dos años hoy tienen ventaja operativa, datos propios y costos de atención menores. El momento de empezar fue ayer. El segundo mejor momento es ahora.',
            'stats': [('77%', 'de PYMES colombianas implementan o quieren IA — Microsoft'), ('54%', 'ya ha dado el primer paso en las Américas'), ('10 días', 'de kick-off a agente en producción'), ('0', 'sistemas existentes que necesitas cambiar en fase 1')],
            'benefits': [('fa-rocket', 'Velocidad de adopción', 'Un agente IA para WhatsApp puede estar operando en 5 días. El ROI es visible en las primeras 4 semanas.'), ('fa-users', 'Toda la organización se beneficia', 'Ventas convierte más. Operaciones responde menos consultas básicas. Dirección tiene datos para decidir.'), ('fa-shield-alt', 'Sin riesgo tecnológico', 'No tocamos tus sistemas existentes. El agente se integra sobre lo que ya tienes: WhatsApp Business y tu equipo.')],
            'steps': [('Diagnóstico digital', 'Evaluamos tu madurez digital actual y definimos el roadmap más realista para tu etapa.'), ('Quick wins', 'Implementamos las automatizaciones de mayor impacto inmediato para generar confianza interna.'), ('Escala sostenible', 'Con los aprendizajes del piloto, construimos la arquitectura de largo plazo.')],
            'faqs': [('¿Por dónde empezar la transformación digital con IA?', 'Por el proceso que más duele hoy: generalmente es la atención al cliente o la generación de leads. Ahí es donde la IA tiene impacto inmediato.'), ('¿Cuánto tiempo toma la transformación digital?', 'Las primeras mejoras tangibles se ven en 30-60 días. La transformación profunda es un proceso de 12-24 meses. Pero el retorno empieza desde el día 1.'), ('¿Necesitamos cambiar toda nuestra tecnología?', 'No. Empezamos sobre lo que ya tienes. WhatsApp Business, tu CRM actual, tu calendario. La IA se integra, no reemplaza.'), ('¿Cómo medimos el éxito?', 'Velocidad de respuesta, tasa de conversión, satisfacción del cliente, horas ahorradas y reducción de costos operativos.')],
        },
        'ia-para-pymes': {
            'intro': 'Hagamos la comparación real. Un asesor de atención al cliente en Colombia cuesta en promedio COP 1.100.000 de salario más el 30% en prestaciones sociales: COP 1.430.000 al mes, cerca de USD 355. Atiende entre 8 y 10 horas al día, máximo 60-80 conversaciones diarias, y tiene días libres, vacaciones y días de incapacidad. Un agente IA para WhatsApp parte desde USD 79 al mes, trabaja las 24 horas los 365 días, y maneja conversaciones simultáneas sin límite. No es que la IA sea "buena para las PYMES": es que hace el trabajo de un asesor a menos de una cuarta parte del costo.',
            'intro2': 'El 55% de las PYMES colombianas cita el costo como la principal barrera para adoptar IA (encuesta Microsoft 2025). Es el argumento equivocado: el costo de no tener IA es más alto que el de tenerla. Cada cliente que escribe y no recibe respuesta en 5 minutos tiene una alta probabilidad de no volver.',
            'callout': 'La IA no le quita el trabajo a nadie en una PYME. Le quita al dueño la tarea de responder WhatsApp a las 11pm cuando ya está agotado, y le da al equipo tiempo para hacer lo que realmente genera valor.',
            'stats': [('USD 79/mes', 'vs USD 355/mes de un asesor en Colombia'), ('55%', 'de PYMES cita el costo como barrera — Microsoft 2025'), ('∞', 'conversaciones simultáneas sin costo adicional'), ('48h', 'para tener el agente operando')],
            'benefits': [('fa-dollar-sign', 'Costo accesible', 'Planes desde USD 79/mes. Menos que contratar medio tiempo de atención al cliente, con el triple de capacidad.'), ('fa-expand-arrows-alt', 'Escala sin contratar', 'Maneja 10 o 1.000 conversaciones simultáneas con el mismo costo. La IA crece con tu negocio sin escalar costos.'), ('fa-star', 'Experiencia de gran empresa', 'Tus clientes reciben la misma calidad de atención que ofrecen las grandes marcas: inmediata, precisa y 24/7.')],
            'steps': [('Onboarding express', 'En 48 horas configuramos el agente con la información básica de tu PYME.'), ('Ajuste fino', 'Durante los primeros 14 días afinamos respuestas según las conversaciones reales.'), ('Crecimiento', 'Con el agente funcionando, tu equipo puede enfocarse en crecer el negocio, no en responder mensajes.')],
            'faqs': [('¿Funciona para negocios muy pequeños?', 'Sí. Si tienes WhatsApp Business y recibes más de 10 mensajes al día, ya te conviene automatizar.'), ('¿Cuánto cuesta para una PYME en Colombia?', 'Desde COP 320.000/mes. Ajustamos los precios a la moneda y poder adquisitivo de cada país LATAM.'), ('¿Necesito equipo técnico?', 'No. Nos encargamos de todo. Solo necesitas aprobar el contenido de entrenamiento y conectar tu WhatsApp Business.'), ('¿Puedo cancelar cuando quiera?', 'Sí. Trabajamos mes a mes. Sin contratos anuales ni penalidades por cancelación.')],
        },
        'ia-para-retail': {
            'intro': 'El comercio por WhatsApp en LATAM creció un 107% en México y un 111% en Argentina en 2025. El 75% de las empresas mexicanas ya integra canales de mensajería en el proceso de compra. Estos no son proyectos piloto: son el canal principal de ventas para miles de retailers que descubrieron que la conversión en WhatsApp es hasta 10 veces mayor que por email. La tasa de apertura de un mensaje de WhatsApp es del 98%; la de un email de marketing, 21,5%.',
            'intro2': 'El cliente de retail en LATAM no espera. Pregunta por stock a las 8pm, compara con la competencia en 3 minutos, y decide en esa misma conversación. Si tu respuesta llega al día siguiente, la venta ya está perdida. Un agente IA responde en segundos con disponibilidad real, recomienda según el historial del cliente y cierra la venta sin que ningún vendedor tenga que abrir el teléfono.',
            'callout': 'Las conversiones en WhatsApp con IA alcanzan el 45-60% de los chats iniciados. Por email, esa misma campaña convierte entre el 2% y el 5%. Si tienes tienda y aún priorizas el email sobre WhatsApp, estás invirtiendo en el canal equivocado.',
            'stats': [('107%', 'crecimiento comercio WhatsApp en México en 2025'), ('10x', 'mayor conversión en WhatsApp vs email'), ('98%', 'tasa de apertura de WhatsApp vs 21.5% email'), ('75%', 'de empresas MX integran mensajería en el proceso de compra')],
            'benefits': [('fa-search', 'Búsqueda de productos inteligente', 'El cliente describe lo que busca y el agente recomienda opciones de tu catálogo al instante.'), ('fa-shopping-bag', 'Proceso de compra guiado', 'El agente acompaña al cliente desde la consulta hasta la confirmación del pedido sin fricción.'), ('fa-redo', 'Recuperación de abandono', 'Detecta clientes que consultaron pero no compraron y los contacta proactivamente con incentivos personalizados.')],
            'steps': [('Catálogo digital', 'Cargamos tu catálogo completo: fotos, precios, variantes y stock.'), ('Flujos de compra', 'Configuramos el proceso de consulta, cotización y confirmación de pedido.'), ('Recuperación automática', 'Activamos secuencias de seguimiento para leads que no convirtieron.')],
            'faqs': [('¿Se puede integrar con mi sistema de inventario?', 'Sí. Conectamos con los principales sistemas de inventario y e-commerce para que el agente conozca el stock en tiempo real.'), ('¿El agente puede procesar pagos?', 'El agente puede enviar links de pago y confirmar transacciones. La pasarela de pago la configuras tú.'), ('¿Funciona para tiendas físicas y online?', 'Sí para ambas. Para tiendas físicas gestiona reservas de productos. Para online acompaña todo el funnel de compra.'), ('¿Cómo maneja las devoluciones?', 'El agente recopila la información de la devolución y escala al equipo humano con todos los datos listos.')],
        },
        'ia-para-salud': {
            'intro': 'Las clínicas dentales en México reportan tasas de no-show del 25% al 40%. En un consultorio con 20 pacientes al día, eso son entre 5 y 8 sillas vacías diarias. Si la consulta promedio cuesta COP 150.000-300.000 (o su equivalente en MXN), ocho citas perdidas representan entre COP 1.200.000 y 2.400.000 al día en ingresos que no entraron. Al mes, eso puede ser COP 25-50 millones perdidos por no-shows que un recordatorio de WhatsApp podría haber evitado.',
            'intro2': 'Con recordatorios automáticos vía WhatsApp, los estudios del sector muestran que la tasa de no-show cae al 8-12% y la conversión de lead a cita sube al 60-75%. No es tecnología experimental: es un proceso comprobado que las clínicas con más citas ya usan mientras las que tienen lista de espera siguen coordinando todo por llamadas.',
            'callout': 'El tiempo que una recepcionista gasta en llamadas de confirmación de citas —entre 30 y 45 minutos por cada paciente no confirmado— puede eliminarse casi por completo. Ese tiempo puede dedicarse a la experiencia del paciente dentro del consultorio.',
            'stats': [('25-40%', 'tasa de no-show en clínicas dentales LATAM'), ('8-12%', 'no-show alcanzable con recordatorios WhatsApp'), ('60-75%', 'conversión lead→cita con agente IA'), ('40h', 'mensuales que recupera una recepcionista típica')],
            'benefits': [('fa-calendar-plus', 'Agendamiento 24/7', 'Los pacientes agendan citas a cualquier hora por WhatsApp. El agente consulta disponibilidad real y confirma en segundos.'), ('fa-bell', 'Reducción de ausentismo', 'Recordatorios automáticos 24h y 2h antes de la cita reducen el ausentismo entre un 30% y 45%.'), ('fa-clipboard-list', 'Triaje inicial', 'El agente recopila síntomas y urgencia antes de la cita, permitiendo al médico prepararse y priorizar correctamente.')],
            'steps': [('Configuración clínica', 'Cargamos horarios, especialidades, médicos disponibles y protocolos de atención.'), ('Integración de agenda', 'Conectamos con tu sistema de agenda actual para sincronización en tiempo real.'), ('Protocolo de escalada', 'Definimos claramente cuándo el agente escala a personal humano en casos de urgencia.')],
            'faqs': [('¿Es seguro para datos de pacientes?', 'Sí. Cumplimos con los estándares de manejo de datos del sector salud. Los datos se transmiten encriptados y no se almacenan en terceros no autorizados.'), ('¿Puede el agente dar diagnósticos?', 'No y nunca lo hace. El agente gestiona la parte administrativa y escala siempre al profesional para cualquier consulta médica.'), ('¿Funciona para clínicas especializadas?', 'Sí. Tenemos experiencia con odontología, dermatología, psicología, fisioterapia y medicina general.'), ('¿Cuánto tiempo toma la implementación?', 'Entre 5 y 10 días hábiles incluyendo la carga de información y pruebas.')],
        },
        'ia-para-restaurantes': {
            'intro': 'El 80% de los clientes prefiere escribir por WhatsApp antes que llamar por teléfono. Para un restaurante, eso significa que la mayoría de las reservas, consultas de menú y pedidos para llevar llegan por texto a cualquier hora del día o la noche. El problema: si el equipo está en servicio a las 8pm, nadie está revisando el celular. Esa reserva para el viernes que llegó el miércoles a las 10pm se perdió sin que te enteraras.',
            'intro2': 'Los restaurantes que han implementado automatización de WhatsApp reportan hasta un 45% más de reservas confirmadas. El margen del negocio mejora un 16% en promedio porque se reducen los no-shows, se recuperan clientes inactivos y el equipo puede enfocarse en el servicio en sala en lugar de coordinar por teléfono.',
            'callout': 'Una reserva que llega a las 11pm y no obtiene respuesta antes del amanecer tiene 70% de probabilidad de cancelarse o de que el cliente reserve en otro lugar. La velocidad de respuesta es la diferencia entre mesa llena y mesa vacía el viernes.',
            'stats': [('80%', 'de clientes prefiere escribir vs llamar'), ('+45%', 'más reservas con automatización WhatsApp'), ('16%', 'mejora de margen con automatización en hostelería'), ('<3 seg', 'tiempo de respuesta del agente IA')],
            'benefits': [('fa-utensils', 'Reservas automáticas', 'El agente verifica disponibilidad y confirma la reserva en tiempo real, sin intervención del equipo.'), ('fa-motorcycle', 'Pedidos para llevar', 'Gestiona pedidos, personaliza por alergias o preferencias y confirma tiempos de entrega automáticamente.'), ('fa-user-clock', 'Recuperación de clientes', 'Identifica clientes que no han visitado en 30+ días y les envía una oferta personalizada para reactivarlos.')],
            'steps': [('Menú digital', 'Cargamos tu menú completo con precios, fotos y opciones de personalización.'), ('Flujos de reserva', 'Configuramos el proceso de reserva, lista de espera y confirmaciones.'), ('Fidelización', 'Activamos secuencias de recuperación para clientes inactivos y fechas especiales.')],
            'faqs': [('¿Puede el agente manejar pedidos a domicilio?', 'Sí. Gestiona el pedido completo, calcula el total y coordina con tu equipo de cocina.'), ('¿Funciona para restaurantes con múltiples sucursales?', 'Sí. Configuramos el agente para dirigir al cliente a la sucursal más cercana o disponible.'), ('¿Cómo maneja las alergias?', 'El agente pregunta activamente por restricciones alimentarias y las agrega como nota al pedido.'), ('¿Se puede integrar con delivery apps?', 'El agente maneja el canal de WhatsApp. La integración con Rappi o iFood requiere desarrollo adicional.')],
        },
        'ia-para-hoteles': {
            'intro': 'Booking.com cobra entre el 15% y el 25% de comisión por cada reserva. Airbnb cobra al huésped hasta el 14% adicional. Una habitación de USD 150 por noche reservada a través de una OTA le deja al hotel entre USD 112 y USD 127. Esa misma habitación reservada directamente por WhatsApp le deja USD 150, más los datos del huésped, más la relación directa para la próxima estadía. El 68% de los viajeros ya pregunta por WhatsApp antes de reservar. Si respondes rápido y bien, puedes convertir esa consulta en reserva directa.',
            'intro2': 'Para los hoteles boutique y hostales de LATAM, la IA multiidioma resuelve el problema que no pueden pagar con personal: atender en inglés y portugués las 24 horas. Un viajero de Brasil que escribe a las 2am preguntando por disponibilidad no espera respuesta hasta las 9am del equipo local. Si el agente responde en portugués en segundos, la reserva es tuya.',
            'callout': 'Cada reserva directa por WhatsApp que reemplaza una de Booking.com recupera entre USD 22 y USD 37 en comisiones. Con un agente IA manejando la consulta inicial, convertir esas consultas en reservas directas es sistemático, no accidental.',
            'stats': [('15-25%', 'comisión OTAs vs 0% por WhatsApp directo'), ('68%', 'de viajeros consulta por WhatsApp antes de reservar'), ('<10 min', 'margen antes de que busquen otro hotel'), ('3 idiomas', 'español, inglés, portugués sin costo extra de personal')],
            'benefits': [('fa-globe', 'Multiidioma automático', 'El agente detecta el idioma del huésped y responde en español, inglés o portugués sin configuración adicional.'), ('fa-bed', 'Reservas directas', 'Evita comisiones de OTAs: el agente toma reservas directas por WhatsApp con confirmación automática.'), ('fa-concierge-bell', 'Servicio al huésped', 'Durante la estadía, el agente resuelve solicitudes de housekeeping, restaurante y check-out sin que el huésped llame a recepción.')],
            'steps': [('Perfil del hotel', 'Cargamos habitaciones, tarifas, políticas y servicios disponibles.'), ('Flujo de reserva', 'Configuramos verificación de disponibilidad, cotización y confirmación de reserva.'), ('Protocolo de estadía', 'Activamos mensajes de bienvenida, guía de servicios y check-out automatizado.')],
            'faqs': [('¿Puede el agente conectarse con el PMS del hotel?', 'Dependiendo del PMS. Tenemos integración con los principales sistemas. Consultamos caso por caso.'), ('¿Cómo maneja las cancelas y cambios?', 'El agente gestiona cambios de fecha y cancelas según la política del hotel, con confirmación automática.'), ('¿Funciona para hostales pequeños?', 'Perfectamente. De hecho, los hostales obtienen mayor beneficio proporcional porque tienen menos personal para atender tantas consultas.'), ('¿En qué idiomas opera?', 'Principalmente español, inglés y portugués. Otros idiomas se evalúan caso a caso.')],
        },
        'ia-para-salones-de-belleza': {
            'intro': 'Calcula el costo real de los no-shows en tu salón. Un servicio de coloración o alisado ocupa entre 90 minutos y 3 horas de una estilista. Si un cliente no llega sin avisar, ese slot es irrecuperable: la estilista no puede atender a nadie más y el tiempo se pierde. En un salón con 4 estilistas y una tasa de no-show del 20%, eso son entre 5 y 10 horas perdidas a la semana. A COP 80.000-150.000 por servicio, hablamos de COP 400.000-1.500.000 semanales en ingresos que no entraron por falta de un recordatorio.',
            'intro2': 'El 11pm es la hora más común en que las clientas escriben para agendar cita del día siguiente. No es que estén siendo desconsideradas: es cuando terminaron su jornada y se acordaron. Si tu salón no tiene un sistema que responda a esa hora, esa clienta agenda en el siguiente salón que sí aparece disponible. Un agente IA verifica la agenda en tiempo real, confirma el turno y envía el recordatorio 24h y 1h antes, sin que nadie en el salón haga nada.',
            'callout': 'Reducir el no-show de un 20% a un 8% en un salón con 4 estilistas puede significar 6-8 servicios adicionales recuperados por semana. Al final del mes, eso es el equivalente a un día completo de ingresos que antes se perdía.',
            'stats': [('35%', 'reducción de no-shows con recordatorios WhatsApp'), ('11pm', 'hora pico de mensajes de agendamiento'), ('+20%', 'ticket promedio con fidelización automática'), ('48h', 'para tener la agenda digital activa')],
            'benefits': [('fa-scissors', 'Agenda inteligente', 'El agente consulta disponibilidad de cada estilista y tipo de servicio en tiempo real para ofrecer opciones precisas.'), ('fa-sms', 'Recordatorios automáticos', 'Envía recordatorios 24h y 1h antes de la cita. Reduce las ausencias hasta un 35%.'), ('fa-gift', 'Fidelización y paquetes', 'Notifica a clientas sobre promociones, paquetes y fechas especiales como cumpleaños para aumentar el ticket promedio.')],
            'steps': [('Catálogo de servicios', 'Cargamos todos tus servicios, tiempos, precios y estilistas disponibles.'), ('Agenda digital', 'Sincronizamos con tu agenda actual o configuramos una nueva completamente manejada por el agente.'), ('Secuencias de fidelización', 'Activamos mensajes automáticos de cumpleaños, inactividad y promociones especiales.')],
            'faqs': [('¿El agente agenda con estilistas específicas?', 'Sí. Las clientas pueden pedir a su estilista favorita o al primero disponible.'), ('¿Cómo maneja los depósitos para citas?', 'El agente puede solicitar depósito y enviar el link de pago correspondiente antes de confirmar la cita.'), ('¿Funciona para salones con varias sedes?', 'Sí. El agente identifica la sede más conveniente para la clienta y gestiona la agenda de cada una.'), ('¿Qué pasa si la clienta llega tarde?', 'El agente puede enviar recordatorio 30 minutos antes y gestionar reprogramación si la clienta avisa que no puede llegar.')],
        },
        'ia-para-inmobiliarias': {
            'intro': 'El tiempo promedio de respuesta de un asesor inmobiliario en LATAM a un lead de WhatsApp es de 917 minutos: más de 15 horas. En ese tiempo, el prospecto ya revisó otras 5 opciones, habló con dos asesores que sí respondieron rápido, y probablemente ya coordinó una visita. El dato más importante del negocio inmobiliario no es cuántas propiedades tienes: es quién responde primero. El 78% de los compradores de bienes raíces termina trabajando con el primer asesor que les contesta.',
            'intro2': 'El 34% de los leads inmobiliarios llega fuera del horario comercial. Si tu equipo atiende de 8am a 6pm, estás perdiendo un tercio de tu demanda sin saberlo. Responder en los primeros 5 minutos aumenta la probabilidad de conversión un 900% versus responder 60 minutos después. Un agente IA responde en segundos, califica con las preguntas correctas (zona, presupuesto, tipo de propiedad, urgencia) y agenda la visita con el asesor disponible, todo en la misma conversación.',
            'callout': '917 minutos es el promedio de respuesta de inmobiliarias LATAM. Si tu equipo responde en 5 minutos, ya tienes ventaja competitiva sobre la mayoría del mercado. Si tienes IA que responde en segundos, la ventaja es absoluta.',
            'stats': [('917 min', 'tiempo promedio de respuesta inmobiliarias LATAM'), ('78%', 'de compradores elige el primer asesor que responde'), ('34%', 'de leads inmobiliarios llegan fuera de horario'), ('900%', 'más conversión respondiendo en 5 min vs 60 min')],
            'benefits': [('fa-filter', 'Calificación automática', 'El agente pregunta zona, presupuesto, tipo de propiedad y urgencia. Solo pasa a tus asesores los leads con perfil de compra.'), ('fa-map-marker-alt', 'Presentación de propiedades', 'Muestra fichas de propiedades relevantes según el perfil del cliente, incluyendo fotos y precios.'), ('fa-handshake', 'Agenda de visitas', 'Coordina visitas directamente con el asesor disponible sin correos de ida y vuelta.')],
            'steps': [('Portafolio digital', 'Cargamos todas las propiedades disponibles con filtros por zona, precio y tipo.'), ('Flujo de calificación', 'Configuramos las preguntas clave para calificar leads según tu criterio.'), ('Agenda con asesores', 'Integramos el calendario de cada asesor para agendar visitas automáticamente.')],
            'faqs': [('¿Puede el agente mostrar fotos de propiedades?', 'Sí. Envía fichas con fotos, planos y link al listado completo directamente por WhatsApp.'), ('¿Cómo maneja leads de arriendos y ventas?', 'El agente detecta el tipo de operación desde la primera pregunta y personaliza el flujo correspondiente.'), ('¿Se integra con portales como Finca Raíz o Properati?', 'Manejamos el canal de WhatsApp. Los portales generan los leads y el agente los convierte.'), ('¿El agente puede dar precios?', 'Sí, los precios que cargues. Para negociación de precio, escala al asesor humano.')],
        },
        'precios-agente-ia-latam': {
            'intro': 'Para comparar bien los precios, necesitas saber qué hay en el mercado. Un chatbot básico para WhatsApp en plataformas LATAM (B2Chat, Whaticket, AsisteClick nivel básico) cuesta entre USD 16 y USD 60 al mes. A eso suma el costo de la API de Meta: mensajes de marketing cuestan ~USD 0.025 por mensaje en Colombia, ~MXN 0.55 en México. Para un volumen de 1.000-3.000 conversaciones al mes, el costo total realista de un chatbot básico es USD 25-80/mes. Un agente IA que entiende lenguaje libre, procesa audios y se integra con tu agenda empieza en USD 79/mes. La diferencia de precio es pequeña; la diferencia en resultados, no.',
            'intro2': 'La comparación que importa no es chatbot vs agente IA: es automatización vs atención manual. Un asesor de atención al cliente en Colombia cuesta USD 355/mes y trabaja 8 horas al día. En México, un asesor cuesta entre MXN 8.000-12.000/mes (USD 400-600) incluyendo prestaciones. Un agente IA a USD 79 trabaja 24 horas, 365 días, con conversaciones ilimitadas. El ROI se ve en el primer mes.',
            'callout': 'Cuando evalúes precios, pide siempre una demo en vivo con preguntas de tu industria real, no un guión preparado. Un agente IA bien entrenado responde correctamente el 85-92% de las consultas. Uno mal configurado, el 40%. La diferencia está en la implementación, no en el precio del plan.',
            'stats': [('USD 25-80', 'costo chatbot básico LATAM (mercado actual)'), ('USD 79', 'plan base agente IA Consultor IA'), ('USD 355-600', 'costo asesor humano en Colombia/México'), ('14 días', 'garantía de devolución sin condiciones')],
            'benefits': [('fa-tag', 'Plan Básico: desde USD 79/mes', 'Hasta 500 conversaciones mensuales. Ideal para PYMES con menos de 20 consultas diarias. Incluye configuración y soporte básico.'), ('fa-star', 'Plan Estándar: desde USD 149/mes', 'Conversaciones ilimitadas para un número de WhatsApp. Integraciones con CRM y calendario. Soporte prioritario.'), ('fa-crown', 'Plan Empresa: desde USD 299/mes', 'Múltiples números, integraciones avanzadas, reportes de analytics y gerente de cuenta dedicado.')],
            'extra_html': '''
    <section class="py-16">
        <div class="container mx-auto px-6 max-w-5xl">
            <h2 class="text-3xl font-header font-bold text-center mb-4 text-zinc-900 dark:text-white">Comparativa de planes 2026</h2>
            <p class="text-center text-gray-2 dark:text-zinc-400 mb-10">Precios en USD. Sin contratos anuales. Cancela cuando quieras.</p>
            <div class="overflow-x-auto rounded-2xl border border-gray-border dark:border-zinc-800">
                <table class="w-full text-sm">
                    <thead>
                        <tr class="bg-zinc-900 dark:bg-zinc-800 text-white">
                            <th class="text-left p-4 font-semibold">Característica</th>
                            <th class="text-center p-4 font-semibold">Básico<br><span class="text-accent font-bold text-base">USD 79/mes</span></th>
                            <th class="text-center p-4 font-semibold border-x border-zinc-700">Estándar<br><span class="text-accent font-bold text-base">USD 149/mes</span></th>
                            <th class="text-center p-4 font-semibold">Empresa<br><span class="text-accent font-bold text-base">USD 299/mes</span></th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-border dark:divide-zinc-800">
                        <tr class="bg-white dark:bg-zinc-900"><td class="p-4 text-zinc-700 dark:text-zinc-300">Conversaciones/mes</td><td class="p-4 text-center">500</td><td class="p-4 text-center border-x border-gray-border dark:border-zinc-800 font-semibold">Ilimitadas</td><td class="p-4 text-center font-semibold">Ilimitadas</td></tr>
                        <tr class="bg-zinc-50 dark:bg-zinc-950"><td class="p-4 text-zinc-700 dark:text-zinc-300">Números de WhatsApp</td><td class="p-4 text-center">1</td><td class="p-4 text-center border-x border-gray-border dark:border-zinc-800">1</td><td class="p-4 text-center font-semibold">Hasta 5</td></tr>
                        <tr class="bg-white dark:bg-zinc-900"><td class="p-4 text-zinc-700 dark:text-zinc-300">Configuración inicial</td><td class="p-4 text-center"><i class="fas fa-check text-green-500"></i></td><td class="p-4 text-center border-x border-gray-border dark:border-zinc-800"><i class="fas fa-check text-green-500"></i></td><td class="p-4 text-center"><i class="fas fa-check text-green-500"></i></td></tr>
                        <tr class="bg-zinc-50 dark:bg-zinc-950"><td class="p-4 text-zinc-700 dark:text-zinc-300">Integración CRM / calendario</td><td class="p-4 text-center text-zinc-400">—</td><td class="p-4 text-center border-x border-gray-border dark:border-zinc-800"><i class="fas fa-check text-green-500"></i></td><td class="p-4 text-center"><i class="fas fa-check text-green-500"></i></td></tr>
                        <tr class="bg-white dark:bg-zinc-900"><td class="p-4 text-zinc-700 dark:text-zinc-300">Reportes de analytics</td><td class="p-4 text-center text-zinc-400">Básico</td><td class="p-4 text-center border-x border-gray-border dark:border-zinc-800">Avanzado</td><td class="p-4 text-center font-semibold">Completo + exportar</td></tr>
                        <tr class="bg-zinc-50 dark:bg-zinc-950"><td class="p-4 text-zinc-700 dark:text-zinc-300">Soporte</td><td class="p-4 text-center">Email</td><td class="p-4 text-center border-x border-gray-border dark:border-zinc-800">Prioritario</td><td class="p-4 text-center font-semibold">Gerente dedicado</td></tr>
                        <tr class="bg-white dark:bg-zinc-900"><td class="p-4 text-zinc-700 dark:text-zinc-300">Garantía de devolución</td><td class="p-4 text-center"><i class="fas fa-check text-green-500"></i> 14 días</td><td class="p-4 text-center border-x border-gray-border dark:border-zinc-800"><i class="fas fa-check text-green-500"></i> 14 días</td><td class="p-4 text-center"><i class="fas fa-check text-green-500"></i> 14 días</td></tr>
                        <tr class="bg-zinc-50 dark:bg-zinc-950"><td class="p-4 text-zinc-700 dark:text-zinc-300">Colombia (COP aprox.)</td><td class="p-4 text-center">~320.000</td><td class="p-4 text-center border-x border-gray-border dark:border-zinc-800">~610.000</td><td class="p-4 text-center">~1.230.000</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>''',
            'steps': [('Consulta gratuita', 'Analizamos tu volumen de conversaciones actual y necesidades específicas.'), ('Propuesta personalizada', 'Presentamos el plan más adecuado con precios exactos en tu moneda local.'), ('Implementación', 'Empezamos en 5 días hábiles. Pagas cuando el agente está funcionando.')],
            'faqs': [('¿Los precios incluyen el número de WhatsApp?', 'No. Debes tener WhatsApp Business con un número propio. Te acompañamos en el proceso de activación si lo necesitas.'), ('¿Hay contrato de permanencia?', 'No. Trabajamos mes a mes. Puedes cancelar cuando quieras sin penalidades.'), ('¿Los precios incluyen IVA?', 'Los precios base son en USD y no incluyen impuestos locales. Para Colombia aplica IVA del 19% sobre el servicio digital.'), ('¿Se puede cambiar de plan?', 'Sí. Puedes escalar o reducir el plan en cualquier momento. El ajuste aplica desde el siguiente mes.')],
        },
        'como-implementar-agente-ia': {
            'intro': 'Lo único que necesitas para empezar es: una lista de las 10 preguntas más frecuentes que recibe tu negocio por WhatsApp, el catálogo o listado de servicios con precios, y el tono de comunicación que quieres que use el agente (formal, cercano, técnico). Con eso, en el kick-off del día 1 ya tenemos suficiente para configurar el 80% del agente. El 20% restante se descubre en los primeros 14 días de conversaciones reales, no en documentos de requisitos de 50 páginas.',
            'intro2': 'El error más costoso que cometen las empresas es esperar tener "todo perfecto" antes de lanzar. Un agente imperfecto que está vivo y aprendiendo de conversaciones reales supera siempre a un proyecto de documentación que lleva tres meses sin producir nada. El perfeccionismo en IA es el enemigo del progreso: lanza en 10 días, mide 30, ajusta con datos.',
            'callout': 'Tu tiempo invertido en el proceso completo es de 3-4 horas distribuidas en 10 días: el kick-off de 60 minutos, la revisión del contenido, y las pruebas finales. El resto lo hacemos nosotros.',
            'stats': [('3-4h', 'tu tiempo total en todo el proceso de implementación'), ('10 días', 'de kick-off a agente en producción'), ('14 días', 'garantía de devolución sin condiciones'), ('30 días', 'de monitoreo y ajustes incluidos post-lanzamiento')],
            'benefits': [('fa-clock', 'En menos de 10 días', 'Desde el primer call hasta el agente funcionando en producción. Rápido porque usamos metodología probada con cientos de implementaciones.'), ('fa-check-double', 'Sin riesgo', 'Los primeros 14 días son de prueba. Si el agente no funciona como esperabas, te devolvemos el dinero.'), ('fa-graduation-cap', 'Capacitación incluida', 'Entrenamos a tu equipo para revisar conversaciones, ajustar respuestas y sacar el máximo provecho del agente.')],
            'steps': [('Kick-off (Día 1)', 'Call de 60 minutos para entender tu negocio, flujos de atención y objetivos del agente.'), ('Entrenamiento (Días 2-5)', 'Cargamos tu información y configuramos los flujos de conversación. Tú apruebas el contenido.'), ('QA y lanzamiento (Días 6-10)', 'Pruebas internas, ajustes finos y activación del agente en producción con monitoreo en tiempo real.')],
            'faqs': [('¿Necesito cambiar mi número de WhatsApp?', 'No. El agente opera sobre tu número actual de WhatsApp Business. Si no tienes cuenta Business, te ayudamos a crearla.'), ('¿Qué información necesito preparar?', 'Lista de preguntas frecuentes, catálogo de servicios/productos con precios, horarios de atención y nombre del negocio. Eso es suficiente para empezar.'), ('¿Cuánto tiempo me toma a mí durante la implementación?', 'Aproximadamente 3-4 horas distribuidas en 10 días: el kick-off, revisión del contenido y pruebas finales.'), ('¿Qué pasa después del lanzamiento?', 'Monitoreo durante 30 días, informe mensual de conversaciones y sesión de optimización a los 30 días.')],
        },
        'agente-ia-vs-chatbot': {
            'intro': 'Seamos honestos: para algunos negocios, un chatbot es suficiente. Si solo necesitas responder "estamos abiertos de 9am a 6pm, lunes a sábado" y mostrar un menú de 4 opciones, un chatbot básico a USD 20/mes hace el trabajo. El problema es que la mayoría de los negocios no tiene eso: tiene clientes que preguntan "¿tienen el modelo X en talla S pero en color azul oscuro?", o "necesito cita para mañana pero solo puedo de 12 a 2pm", o mensajes de voz de 30 segundos explicando un problema. Para esos casos, el chatbot dice "no entendí tu solicitud" y frustra al cliente.',
            'intro2': 'La diferencia técnica es fundamental: un chatbot ejecuta árboles de decisión predefinidos. Un agente IA usa un motor de razonamiento que entiende lenguaje libre, mantiene contexto a lo largo de la conversación y puede acceder a herramientas externas (agenda, catálogo, CRM) para resolver en la misma interacción. La tasa de resolución de un agente IA bien configurado es del 85-92% de conversaciones. La de un chatbot típico, 40-50%.',
            'callout': 'La prueba del 20%: toma el 20% de conversaciones más complejas que recibes en WhatsApp y pregúntate si un menú de opciones fijas las resolvería. Si la respuesta es no, necesitas agente IA.',
            'stats': [('85-92%', 'tasa de resolución agente IA bien configurado'), ('40-50%', 'tasa de resolución chatbot típico'), ('USD 20-60', 'chatbot básico LATAM vs USD 79+ agente IA'), ('0', 'mensajes de voz que un chatbot puede procesar')],
            'benefits': [('fa-comments', 'Agente IA: conversación natural', 'Entiende preguntas en lenguaje libre, con errores de ortografía, jerga local y mensajes de voz. Responde con contexto.'), ('fa-sitemap', 'Chatbot: menús predefinidos', 'Solo responde a opciones preconfiguradas. Si el cliente se sale del flujo, el bot se rompe o dice "no entiendo".'), ('fa-trophy', 'El veredicto', 'Para negocios con conversaciones diversas y clientes exigentes: agente IA. Para FAQs simples con 5 opciones: chatbot puede funcionar.')],
            'extra_html': '''
    <section class="py-16 bg-zinc-50 dark:bg-zinc-900/30">
        <div class="container mx-auto px-6 max-w-5xl">
            <h2 class="text-3xl font-header font-bold text-center mb-10 text-zinc-900 dark:text-white">Chatbot vs Agente IA: comparación completa</h2>
            <div class="overflow-x-auto rounded-2xl border border-gray-border dark:border-zinc-800">
                <table class="w-full text-sm">
                    <thead>
                        <tr class="bg-zinc-900 dark:bg-zinc-800 text-white">
                            <th class="text-left p-4 font-semibold w-2/5">Capacidad</th>
                            <th class="text-center p-4 font-semibold w-[30%]"><i class="fas fa-sitemap mr-2 text-zinc-400"></i>Chatbot tradicional</th>
                            <th class="text-center p-4 font-semibold w-[30%] bg-accent/20"><i class="fas fa-brain mr-2 text-accent"></i>Agente IA</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-border dark:divide-zinc-800">
                        <tr class="bg-white dark:bg-zinc-900"><td class="p-4 text-zinc-700 dark:text-zinc-300 font-medium">Lenguaje natural</td><td class="p-4 text-center text-red-500"><i class="fas fa-times"></i> Solo opciones fijas</td><td class="p-4 text-center text-green-500 bg-accent/5"><i class="fas fa-check"></i> Comprende texto libre</td></tr>
                        <tr class="bg-zinc-50 dark:bg-zinc-950"><td class="p-4 text-zinc-700 dark:text-zinc-300 font-medium">Errores de escritura</td><td class="p-4 text-center text-red-500"><i class="fas fa-times"></i> Falla o ignora</td><td class="p-4 text-center text-green-500 bg-accent/5"><i class="fas fa-check"></i> Entiende igual</td></tr>
                        <tr class="bg-white dark:bg-zinc-900"><td class="p-4 text-zinc-700 dark:text-zinc-300 font-medium">Mensajes de voz</td><td class="p-4 text-center text-red-500"><i class="fas fa-times"></i> No compatible</td><td class="p-4 text-center text-green-500 bg-accent/5"><i class="fas fa-check"></i> Transcribe y responde</td></tr>
                        <tr class="bg-zinc-50 dark:bg-zinc-950"><td class="p-4 text-zinc-700 dark:text-zinc-300 font-medium">Memoria de la conversación</td><td class="p-4 text-center text-red-500"><i class="fas fa-times"></i> Sin contexto</td><td class="p-4 text-center text-green-500 bg-accent/5"><i class="fas fa-check"></i> Recuerda el hilo</td></tr>
                        <tr class="bg-white dark:bg-zinc-900"><td class="p-4 text-zinc-700 dark:text-zinc-300 font-medium">Respuestas fuera del flujo</td><td class="p-4 text-center text-red-500"><i class="fas fa-times"></i> "No entendí"</td><td class="p-4 text-center text-green-500 bg-accent/5"><i class="fas fa-check"></i> Improvisa con contexto</td></tr>
                        <tr class="bg-zinc-50 dark:bg-zinc-950"><td class="p-4 text-zinc-700 dark:text-zinc-300 font-medium">Tasa de resolución</td><td class="p-4 text-center font-medium">~40-50%</td><td class="p-4 text-center font-bold text-accent bg-accent/5">~85-92%</td></tr>
                        <tr class="bg-white dark:bg-zinc-900"><td class="p-4 text-zinc-700 dark:text-zinc-300 font-medium">Escalada inteligente al humano</td><td class="p-4 text-center text-red-500"><i class="fas fa-times"></i> Sin contexto</td><td class="p-4 text-center text-green-500 bg-accent/5"><i class="fas fa-check"></i> Con historial completo</td></tr>
                        <tr class="bg-zinc-50 dark:bg-zinc-950"><td class="p-4 text-zinc-700 dark:text-zinc-300 font-medium">Costo mensual aprox.</td><td class="p-4 text-center">USD 20-60</td><td class="p-4 text-center font-medium bg-accent/5">USD 79-299</td></tr>
                        <tr class="bg-white dark:bg-zinc-900"><td class="p-4 text-zinc-700 dark:text-zinc-300 font-medium">ROI promedio</td><td class="p-4 text-center">Bajo (FAQs)</td><td class="p-4 text-center font-bold text-accent bg-accent/5">Alto (ventas + atención)</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>''',
            'steps': [('Evalúa tu caso', 'Analiza el 20% de conversaciones más difíciles que recibes. Si un chatbot no las manejaría, necesitas agente IA.'), ('Calcula el ROI', 'Compara el costo del agente vs chatbot vs personal humano en tu volumen de conversaciones.'), ('Implementa el correcto', 'Te asesoramos gratis para que elijas la tecnología más adecuada para tu caso específico.')],
            'faqs': [('¿Cuánto más caro es un agente IA vs chatbot?', 'Entre 30-50% más caro que un chatbot básico. Pero la tasa de resolución es 3-4x mayor, lo que se traduce en más conversiones.'), ('¿Los chatbots son obsoletos?', 'Para casos muy simples (horarios, dirección, menú fijo) un chatbot sigue siendo válido. Para ventas y atención compleja, el agente IA es claramente superior.'), ('¿Puedo migrar de chatbot a agente IA?', 'Sí. Si ya tienes un chatbot, migramos la información y flujos al agente IA. El proceso toma 3-5 días adicionales.'), ('¿Qué pasa cuando el agente no sabe responder?', 'El agente IA escala al humano con todo el contexto de la conversación. El chatbot generalmente solo dice "no entendí" sin contexto.')],
        },
        'casos-exito-ia-pymes': {
            'intro': 'Los resultados de IA en PYMES LATAM no son uniformes ni garantizados, y es importante decirlo. Lo que sí es consistente: la mejora siempre aparece primero en la velocidad de respuesta (desde el día 1), luego en la tasa de conversión (semanas 2-4), y finalmente en los ingresos (mes 2-3). Las variaciones dependen de cuán bien está entrenado el agente y de qué tan repetitivo es el tipo de consulta que recibe el negocio.',
            'intro2': 'Los casos que más impacto generan no son siempre los que tienen los números más grandes: son los que cambian la operación diaria del dueño. Una recepcionista de clínica dental que dejó de hacer 40 llamadas de confirmación al mes puede atender mejor a los pacientes que están físicamente en el consultorio. Un dueño de salón que dejó de responder WhatsApp a las 11pm puede descansar. Eso no aparece en una hoja de cálculo pero es el resultado más valioso.',
            'callout': 'Antes de implementar, mide tres cosas: tu tasa de respuesta actual (¿cuántos mensajes se quedan sin respuesta en las primeras 2 horas?), tu tasa de conversión lead→venta, y tu tasa de no-show si aplica. Con esos datos de partida, podrás medir el impacto real del agente IA en los primeros 30 días.',
            'stats': [('28%→11%', 'no-show en clínica dental Bogotá (caso representativo)'), ('+34%', 'reservas restaurante CDMX en 60 días'), ('3%→8%', 'cierre inmobiliaria Buenos Aires'), ('40h', 'mensuales recuperadas por recepcionista típica')],
            'benefits': [('fa-tooth', 'Clínica dental en Bogotá', 'Redujo el ausentismo de citas de 28% a 11% con recordatorios automáticos. Recuperó 40 horas mensuales de tiempo de recepcionista.'), ('fa-utensils', 'Restaurante en Ciudad de México', 'Aumentó reservas confirmadas en 34% en los primeros 60 días. El agente maneja el 85% de las conversaciones sin intervención humana.'), ('fa-building', 'Inmobiliaria en Buenos Aires', 'Pasó de calificar 15 leads/semana manualmente a 80+ leads/semana con el agente. Tasa de cierre mejoró del 3% al 8%.')],
            'extra_html': '''
    <section class="py-16">
        <div class="container mx-auto px-6 max-w-5xl">
            <h2 class="text-3xl font-header font-bold text-center mb-10 text-zinc-900 dark:text-white">Resultados por industria</h2>
            <div class="overflow-x-auto rounded-2xl border border-gray-border dark:border-zinc-800">
                <table class="w-full text-sm">
                    <thead>
                        <tr class="bg-zinc-900 dark:bg-zinc-800 text-white">
                            <th class="text-left p-4 font-semibold">Industria</th>
                            <th class="text-center p-4 font-semibold">Antes</th>
                            <th class="text-center p-4 font-semibold">Después (60 días)</th>
                            <th class="text-center p-4 font-semibold">Impacto principal</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-border dark:divide-zinc-800">
                        <tr class="bg-white dark:bg-zinc-900"><td class="p-4 font-medium text-zinc-800 dark:text-zinc-200"><i class="fas fa-tooth text-accent mr-2"></i>Clínica dental</td><td class="p-4 text-center text-zinc-500">28% ausentismo</td><td class="p-4 text-center font-bold text-green-600">11% ausentismo</td><td class="p-4 text-center text-sm text-zinc-600 dark:text-zinc-400">Recordatorios 24h y 2h antes</td></tr>
                        <tr class="bg-zinc-50 dark:bg-zinc-950"><td class="p-4 font-medium text-zinc-800 dark:text-zinc-200"><i class="fas fa-utensils text-accent mr-2"></i>Restaurante</td><td class="p-4 text-center text-zinc-500">45 reservas/sem</td><td class="p-4 text-center font-bold text-green-600">60+ reservas/sem</td><td class="p-4 text-center text-sm text-zinc-600 dark:text-zinc-400">Respuesta inmediata 24/7</td></tr>
                        <tr class="bg-white dark:bg-zinc-900"><td class="p-4 font-medium text-zinc-800 dark:text-zinc-200"><i class="fas fa-building text-accent mr-2"></i>Inmobiliaria</td><td class="p-4 text-center text-zinc-500">15 leads/sem calificados</td><td class="p-4 text-center font-bold text-green-600">80+ leads/sem</td><td class="p-4 text-center text-sm text-zinc-600 dark:text-zinc-400">Calificación automática</td></tr>
                        <tr class="bg-zinc-50 dark:bg-zinc-950"><td class="p-4 font-medium text-zinc-800 dark:text-zinc-200"><i class="fas fa-scissors text-accent mr-2"></i>Salón de belleza</td><td class="p-4 text-center text-zinc-500">35% citas sin confirmar</td><td class="p-4 text-center font-bold text-green-600">8% sin confirmar</td><td class="p-4 text-center text-sm text-zinc-600 dark:text-zinc-400">Agenda + recordatorios</td></tr>
                        <tr class="bg-white dark:bg-zinc-900"><td class="p-4 font-medium text-zinc-800 dark:text-zinc-200"><i class="fas fa-bed text-accent mr-2"></i>Hotel boutique</td><td class="p-4 text-center text-zinc-500">18% conv. desde WhatsApp</td><td class="p-4 text-center font-bold text-green-600">31% conv. desde WhatsApp</td><td class="p-4 text-center text-sm text-zinc-600 dark:text-zinc-400">Respuesta &lt;3 seg. multiidioma</td></tr>
                        <tr class="bg-zinc-50 dark:bg-zinc-950"><td class="p-4 font-medium text-zinc-800 dark:text-zinc-200"><i class="fas fa-shopping-bag text-accent mr-2"></i>Retail</td><td class="p-4 text-center text-zinc-500">USD 45 ticket promedio</td><td class="p-4 text-center font-bold text-green-600">USD 67 ticket promedio</td><td class="p-4 text-center text-sm text-zinc-600 dark:text-zinc-400">Recomendación y upsell</td></tr>
                    </tbody>
                </table>
            </div>
            <p class="text-xs text-center text-zinc-400 dark:text-zinc-600 mt-4">Datos representativos de clientes reales. Los resultados varían según el negocio, la industria y la implementación.</p>
        </div>
    </section>''',
            'steps': [('Mide antes', 'Antes de implementar, registra tu tasa de respuesta, tiempo promedio de atención y conversión actual.'), ('Implementa', 'Lanza el agente con los flujos básicos y mide semanalmente durante el primer mes.'), ('Compara y escala', 'Con los datos reales, optimiza y expande a más canales y procesos.')],
            'faqs': [('¿Estos resultados están garantizados?', 'No garantizamos números específicos porque dependen del negocio, la industria y cómo se implemente. Sí garantizamos que si en 14 días no ves mejora, te devolvemos el dinero.'), ('¿Puedo hablar con clientes actuales de Consultor IA?', 'Sí. En la demo gratuita podemos conectarte con un cliente de tu misma industria para que escuches su experiencia directamente.'), ('¿Cuánto tiempo tarda en verse el primer impacto?', 'La velocidad de respuesta mejora desde el día 1. Las métricas de conversión suelen mejorar en las primeras 2-4 semanas.'), ('¿Qué industrias tienen mejores resultados?', 'Salud (por la reducción de ausentismo), restaurantes (por el volumen de reservas) e inmobiliarias (por la calificación de leads) son los casos con mayor ROI documentado.')],
        },
    }

    data = PILLAR_DATA.get(slug, {
        'intro': f'La inteligencia artificial está transformando los negocios LATAM. Descubre cómo implementar {kw} para mejorar tu atención al cliente y aumentar tus ventas.',
        'intro2': 'Nuestros agentes IA para WhatsApp trabajan 24/7, responden en segundos y se adaptan completamente a tu negocio.',
        'stats': [('73%', 'de PYMES LATAM pierde clientes por respuesta tardía'), ('3 seg', 'tiempo de respuesta del agente IA'), ('40%', 'más conversiones vs. atención manual'), ('5-10', 'días de implementación')],
        'benefits': [('fa-robot', 'Automatización inteligente', 'Responde clientes, agenda citas y cierra ventas automáticamente.'), ('fa-chart-line', 'Más resultados', 'Aumenta conversiones y reduce costos operativos desde el primer mes.'), ('fa-headset', 'Soporte incluido', 'Acompañamiento completo durante la implementación y el primer mes.')],
        'steps': [('Diagnóstico', 'Analizamos tu negocio y definimos la mejor estrategia.'), ('Implementación', 'Configuramos y entrenamos el agente en 5-10 días.'), ('Optimización', 'Ajustamos basándonos en datos reales del primer mes.')],
        'faqs': [('¿Cuánto cuesta?', 'Desde USD 79/mes dependiendo del volumen y las integraciones necesarias.'), ('¿Cuánto tarda la implementación?', 'Entre 5 y 10 días hábiles desde el kick-off hasta el lanzamiento.'), ('¿Necesito conocimientos técnicos?', 'No. Nos encargamos de todo el proceso técnico.'), ('¿Funciona para mi industria?', 'Sí. Tenemos experiencia en más de 10 industrias LATAM.')],
    })

    intro = data['intro']
    intro2 = data['intro2']
    stats = data.get('stats', [])
    benefits = data['benefits']
    steps = data['steps']
    faqs = data['faqs']
    extra_html = data.get('extra_html', '')
    callout = data.get('callout', '')

    # Build callout block
    callout_html = ''
    if callout:
        callout_html = f'''<div class="mt-8 border-l-4 border-accent pl-6 py-1">
                <p class="text-xl font-medium text-zinc-800 dark:text-zinc-100 leading-relaxed">{callout}</p>
            </div>'''

    # Build stats strip
    stats_html = ''
    if stats:
        stats_items = ''
        for value, label in stats:
            stats_items += f'''
            <div class="text-center px-6 py-4 border-b md:border-b-0 md:border-r border-zinc-200 dark:border-zinc-800 last:border-0">
                <div class="text-3xl md:text-4xl font-header font-bold text-zinc-900 dark:text-white mb-1">{value}</div>
                <div class="text-sm text-gray-2 dark:text-zinc-400">{label}</div>
            </div>'''
        stats_html = f'''
    <!-- Stats strip -->
    <section class="border-b border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900">
        <div class="container mx-auto px-6 max-w-5xl">
            <div class="grid grid-cols-2 md:grid-cols-4">
                {stats_items}
            </div>
        </div>
    </section>'''

    # Build benefits cards
    benefits_html = ''
    for icon, title, desc in benefits:
        benefits_html += f'''
        <div class="bg-white dark:bg-zinc-900 border border-gray-border dark:border-zinc-800 rounded-3xl p-8 transition-all duration-300">
            <div class="w-14 h-14 bg-accent/10 rounded-2xl flex items-center justify-center mb-5">
                <i class="fas {icon} text-2xl text-accent"></i>
            </div>
            <h3 class="font-header font-bold text-xl mb-3 text-zinc-900 dark:text-white">{title}</h3>
            <p class="text-gray-2 dark:text-zinc-400 leading-relaxed">{desc}</p>
        </div>'''

    # Build steps
    steps_html = ''
    for i, (title, desc) in enumerate(steps, 1):
        steps_html += f'''
        <div class="flex gap-6 items-start">
            <div class="w-12 h-12 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 font-bold text-lg flex items-center justify-center flex-shrink-0">{i}</div>
            <div>
                <h3 class="font-header font-bold text-lg mb-2 text-zinc-900 dark:text-white">{title}</h3>
                <p class="text-gray-2 dark:text-zinc-400 leading-relaxed">{desc}</p>
            </div>
        </div>'''

    # Build FAQs
    faqs_html = ''
    for question, answer in faqs:
        faqs_html += f'''
        <details class="group border border-gray-border dark:border-zinc-800 rounded-2xl overflow-hidden">
            <summary class="flex items-center justify-between p-6 cursor-pointer font-semibold text-zinc-900 dark:text-white hover:bg-zinc-50 dark:hover:bg-zinc-900/50 transition-colors">
                {question}
                <i class="fas fa-chevron-down text-gray-2 dark:text-zinc-500 group-open:rotate-180 transition-transform duration-200 flex-shrink-0 ml-4"></i>
            </summary>
            <div class="px-6 pb-6 text-gray-2 dark:text-zinc-400 leading-relaxed border-t border-gray-border dark:border-zinc-800 pt-4">
                {answer}
            </div>
        </details>'''

    return f'''
    <!-- Intro -->
    <section class="py-16">
        <div class="container mx-auto px-6 max-w-4xl">
            <div class="prose max-w-none">
                <p class="text-lg text-zinc-700 dark:text-zinc-300 leading-relaxed mb-6">{intro}</p>
                <p class="text-lg text-zinc-700 dark:text-zinc-300 leading-relaxed">{intro2}</p>
                {callout_html}
            </div>
        </div>
    </section>

    {stats_html}

    <!-- Benefits -->
    <section class="py-16 bg-zinc-50 dark:bg-zinc-900/30">
        <div class="container mx-auto px-6 max-w-6xl">
            <h2 class="text-3xl font-header font-bold text-center mb-12 text-zinc-900 dark:text-white">¿Por qué elegir esta solución?</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                {benefits_html}
            </div>
        </div>
    </section>

    {extra_html}

    <!-- How it works -->
    <section class="py-16">
        <div class="container mx-auto px-6 max-w-4xl">
            <h2 class="text-3xl font-header font-bold text-center mb-12 text-zinc-900 dark:text-white">Cómo funciona</h2>
            <div class="flex flex-col gap-10">
                {steps_html}
            </div>
        </div>
    </section>

    <!-- FAQ -->
    <section class="py-16 bg-zinc-50 dark:bg-zinc-900/30">
        <div class="container mx-auto px-6 max-w-3xl">
            <h2 class="text-3xl font-header font-bold text-center mb-12 text-zinc-900 dark:text-white">Preguntas frecuentes</h2>
            <div class="flex flex-col gap-4">
                {faqs_html}
            </div>
        </div>
    </section>'''

def setup_dist():

    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)
    else:
        # Delete everything inside DIST_DIR except .git and blog
        for filename in os.listdir(DIST_DIR):
            if filename not in ['.git', 'Dosckerfile', 'Dockerfile', 'blog', '_redirects']:
                file_path = os.path.join(DIST_DIR, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, "images"), exist_ok=True)
    if os.path.exists("images"):
        # Copy base images including subdirectories
        shutil.copytree("images", os.path.join(DIST_DIR, "images"), dirs_exist_ok=True)
    if os.path.exists("js"):
        # Copy js folder
        shutil.copytree("js", os.path.join(DIST_DIR, "js"), dirs_exist_ok=True)

def get_mega_menu(data):
    # data is a list of dicts (rows)
    # Structure: Industria -> Pais -> list of (Ciudad, URL)
    tree = {}
    for row in data:
        if row.get('Estado') != 'PUBLICAR': continue
        ind = row['Industria']
        pais = row['País']
        ciudad = row['Ciudad']
        url = row['URL_Final']
        
        if ind not in tree:
            tree[ind] = {}
        if pais not in tree[ind]:
            tree[ind][pais] = []
            
        tree[ind][pais].append((ciudad, url))
        
    html = '<ul class="text-sm">'
    for ind, paises in tree.items():
        html += f'<li class="group/ind relative py-2.5 px-2 flex items-center justify-between cursor-pointer rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800/50">'
        html += f'<span class="font-normal text-zinc-900 dark:text-zinc-100 group-hover/ind:text-brand dark:group-hover/ind:text-brand-light transition-colors">{ind}</span>'
        html += f'<i class="fas fa-chevron-right text-[10px] text-zinc-400 dark:text-zinc-600"></i>'
        
        # Paises submenu
        html += f'<div class="absolute left-full top-0 pl-2 w-48 hidden group-hover/ind:block z-50">'
        html += f'<div class="bg-white/95 dark:bg-zinc-950/95 backdrop-blur-xl border border-gray-200 dark:border-zinc-800 shadow-2xl rounded-xl p-2">'
        html += f'<ul class="space-y-0.5">'
        
        for pais, ciudades in paises.items():
            html += f'<li class="group/pais relative py-2 px-3 flex items-center justify-between cursor-pointer rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800/50">'
            html += f'<span class="font-normal text-zinc-700 dark:text-zinc-300 group-hover/pais:text-brand dark:group-hover/pais:text-brand-light transition-colors">{pais}</span>'
            html += f'<i class="fas fa-chevron-right text-[10px] text-zinc-400 dark:text-zinc-600"></i>'
            
            # Cities submenu
            html += f'<div class="absolute left-full top-0 pl-2 w-48 hidden group-hover/pais:block z-50">'
            html += f'<div class="bg-white/95 dark:bg-zinc-950/95 backdrop-blur-xl border border-gray-200 dark:border-zinc-800 shadow-2xl rounded-xl p-2">'
            html += f'<ul class="space-y-0.5">'
            for ciudad, url in ciudades:
                html += f'<li><a href="{url}" class="block py-1.5 px-3 rounded-lg text-zinc-500 dark:text-zinc-400 hover:text-brand dark:hover:text-brand-light hover:bg-brand/5 dark:hover:bg-brand/10 transition-all duration-200">{ciudad}</a></li>'
            html += f'</ul></div></div></li>'
            
        html += f'</ul></div></div></li>'
    html += '</ul>'
    return html

def apply_jargon(text, pais):
    # Determine which dictionary to use based on the country
    jargon = JARGON_DICT.get(pais, JARGON_DICT['Default'])
    
    # Replace all jargon placeholders found in the text
    for key, value in jargon.items():
        if key in text:
            text = text.replace(key, value)
    
    return text

def build_servicios_cards(row):
    ind = row.get('Industria', '')
    cards = INDUSTRY_DATA.get(ind, {}).get('cards', [])
    html = ""
    for card in cards:
        html += f'''
        <div class="bg-[#FDFBF7] dark:bg-zinc-900 border border-gray-border dark:border-zinc-800 rounded-3xl p-8 transition-all duration-300 group">
            <div class="w-14 h-14 bg-brand/10 dark:bg-brand/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <i class="{card['icon']} text-2xl text-brand dark:text-brand-light"></i>
            </div>
            <h3 class="font-header font-bold text-xl mb-3">{card['title']}</h3>
            <p class="text-gray-500 dark:text-slate-400 text-sm leading-relaxed">{card['desc']}</p>
        </div>
        '''
    return html

def get_autocomplete_suggestions(query, cache):
    import urllib.request
    import urllib.parse
    import json
    import time
    
    if not query:
        return []
        
    query_clean = query.strip().lower()
    if cache is not None and query_clean in cache:
        return cache[query_clean]
        
    url = f"https://suggestqueries.google.com/complete/search?client=chrome&q={urllib.parse.quote(query_clean)}"
    
    # Delay de cortesía de 0.2s para evitar cualquier tipo de baneo de IP
    time.sleep(0.2)
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                content = response.read().decode('utf-8', errors='ignore')
                data = json.loads(content)
                suggestions = data[1] if len(data) > 1 else []
                if cache is not None:
                    cache[query_clean] = suggestions
                print(f"API Autocomplete: '{query_clean}' -> Extraídas {len(suggestions)} sugerencias")
                return suggestions
    except Exception as e:
        print(f"Error al consultar autocomplete para '{query_clean}': {e}")
        
    return []

def build_faqs(row, cache=None):
    ind = row.get('Industria', '')
    faqs = INDUSTRY_DATA.get(ind, {}).get('faqs', [])
    
    questions = [(faq['q'], faq['a']) for faq in faqs]
    # Add general FAQs from the row to bulk it up
    questions.extend([
        (row.get('FAQ_General_1_P'), row.get('FAQ_General_1_R')),
        (row.get('FAQ_General_2_P'), row.get('FAQ_General_2_R')),
        (row.get('FAQ_General_3_P'), row.get('FAQ_General_3_R'))
    ])
    
    # Método B: Enriquecimiento dinámico mediante autocompletado de Google
    if cache is not None:
        ind_singular = row.get('Industria_Singular', '').lower()
        ciudad = row.get('Ciudad', '')
        if ind_singular and ciudad:
            query = f"chatbot whatsapp {ind_singular} {ciudad}"
            suggestions = get_autocomplete_suggestions(query, cache)
            
            # Filtrar sugerencias válidas
            valid_suggestions = []
            for sug in suggestions:
                sug_clean = sug.strip().lower()
                if sug_clean != query.lower() and len(sug_clean) > 3:
                    if sug_clean not in valid_suggestions:
                        valid_suggestions.append(sug_clean)
            
            # Inyectar hasta 2 preguntas y respuestas dinámicas con keywords locales sugeridas
            for sug in valid_suggestions[:2]:
                sug_title = sug.title()
                q_sug = f"¿Ofrecen soluciones personalizadas sobre '{sug_title}'?"
                a_sug = f"Sí. En {ciudad} ayudamos a los negocios de {row.get('Industria_Singular', 'la industria')} a resolver búsquedas específicas sobre '{sug_title}'. Nuestros agentes de Inteligencia Artificial para WhatsApp automatizan la comunicación, gestionan bases de datos en tiempo real y optimizan la conversión local. Contáctanos para conocer más detalles."
                questions.append((q_sug, a_sug))
                
    html = ""
    schema_entities = []
    
    for q, a in questions:
        if q and a:
            html += f'''
            <details class="faq-item group">
                <summary>{q}</summary>
                <p>{a}</p>
            </details>
            '''
            schema_entities.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            })
            
    schema_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": schema_entities
    }, ensure_ascii=False)
    
    schema_script = f'<script type="application/ld+json">\n{schema_json}\n</script>'
    return html, schema_script

def build_ciudades_hermanas(row, data):
    hermanas_names = [c.strip() for c in row.get('Ciudades_Hermanas', '').split('|') if c.strip()]
    if not hermanas_names:
        return ""
        
    html = ""
    for r in data:
        if r['Estado'] == 'PUBLICAR' and r['Ciudad'] in hermanas_names and r['Industria'] == row['Industria']:
            html += f'<a href="{r["URL_Final"]}" class="card-ciudad">{r["Ciudad"]}</a>'
        return html

def build_dynamic_eeat_html(row):
    html_content = row.get('Contenido_EEAT', '')
    if not html_content:
        return ""
    
    # Extraer H2
    h2_match = re.search(r'<h2[^>]*>(.*?)</h2>', html_content, re.DOTALL | re.IGNORECASE)
    h2_text = h2_match.group(1).strip() if h2_match else ""
    
    # Extraer H3
    h3_match = re.search(r'<h3[^>]*>(.*?)</h3>', html_content, re.DOTALL | re.IGNORECASE)
    h3_text = h3_match.group(1).strip() if h3_match else ""
    
    # Extraer párrafos
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL | re.IGNORECASE)
    paragraphs = [p.strip() for p in paragraphs]
    
    if not h2_text or not paragraphs:
        return html_content
        
    p_extra_html = ""
    
    # Segmentación inteligente de párrafos
    if len(paragraphs) == 3:
        p1_lead = paragraphs[0]
        p2_lead = paragraphs[1]
        p3_lead = paragraphs[2]
    elif len(paragraphs) >= 4:
        p1_lead = paragraphs[0]
        p2_lead = paragraphs[1]
        p3_lead = paragraphs[-1]
        
        # El párrafo extra es el intermedio (normalmente el de Consultor IA, índice 2)
        p_extra = paragraphs[2]
        p_extra_html = f"""
        <div class="mt-16 pt-8 border-t border-zinc-100 dark:border-zinc-800/80 max-w-4xl mx-auto text-center">
            <p class="text-base md:text-[17px] font-medium text-zinc-600 dark:text-zinc-400 leading-relaxed">
                {p_extra}
            </p>
        </div>
        """
    else:
        p1_lead = paragraphs[0]
        p2_lead = ""
        p3_lead = paragraphs[-1] if len(paragraphs) > 1 else ""

    wa_bubble_html = ""
    # Buscar texto entre comillas dobles y asteriscos, o simplemente entre asteriscos
    wa_match = re.search(r'"\*(.*?)\*"|\*(.*?)\*', p3_lead)
    if wa_match:
        wa_text = wa_match.group(1) or wa_match.group(2)
        if wa_text:
            wa_bubble_html = f"""
            <div class="mt-6 p-4 bg-[#E2F8CB] dark:bg-[#0b5c49] rounded-2xl rounded-tr-none border border-[#b2dca2]/40 dark:border-[#008f72]/20 shadow-md max-w-[95%] ml-auto relative">
                <p class="text-xs text-zinc-800 dark:text-zinc-100 font-sans leading-normal">
                    {wa_text}
                </p>
                <span class="absolute top-0 right-[-8px] w-0 h-0 border-t-[8px] border-t-[#E2F8CB] dark:border-t-[#0b5c49] border-r-[8px] border-r-transparent"></span>
                <div class="text-[9px] text-zinc-500 dark:text-zinc-300 text-right mt-1">
                    <i class="fas fa-check-double text-sky-500 mr-0.5"></i> Entregado
                </div>
            </div>
            """
    
    # Formatear párrafos de las columnas (usando estilos grises/neutros elegantes, no el negro fuerte)
    p1_html = f'<p class="text-base md:text-[17px] font-medium text-zinc-600 dark:text-zinc-400 leading-relaxed">{p1_lead}</p>'
    p2_html = f'<p class="text-base md:text-[17px] font-medium text-zinc-600 dark:text-zinc-400 leading-relaxed">{p2_lead}</p>'
    p3_html = f'<p class="text-base md:text-[17px] font-medium text-zinc-600 dark:text-zinc-400 leading-relaxed">{p3_lead}</p>'
    
    new_html = f"""
    <section class="py-24 bg-white dark:bg-zinc-950 border-t border-gray-100 dark:border-zinc-900 relative overflow-hidden">
        <div class="absolute top-1/2 left-0 w-72 h-72 bg-[#E8DAC1]/10 dark:bg-brand/5 rounded-full blur-3xl pointer-events-none"></div>
        
        <div class="container mx-auto px-4 max-w-6xl relative z-10">
            <!-- Título Principal -->
            <div class="text-center mb-20 max-w-3xl mx-auto">
                <span class="text-brand dark:text-brand-light font-body text-xs font-bold uppercase tracking-widest mb-3 block">Flujo de Trabajo y Contexto</span>
                <h2 class="text-3xl md:text-5xl font-header font-bold text-zinc-900 dark:text-white leading-tight">
                    {h2_text}
                </h2>
            </div>
            
            <!-- Contenedor del Flujo Horizontal -->
            <div class="relative">
                <!-- Línea de conexión horizontal con degradado (solo en desktop) -->
                <div class="absolute top-4 left-4 right-4 h-[2px] bg-gradient-to-r from-zinc-200 via-brand/30 to-zinc-200 dark:from-zinc-800 dark:via-brand-light/30 dark:to-zinc-800 hidden lg:block -z-10"></div>
                
                <div class="grid lg:grid-cols-3 gap-12 lg:gap-16 items-stretch">
                    <!-- Paso 1: La Oportunidad -->
                    <div class="flex flex-col items-start relative group">
                        <div class="w-8 h-8 rounded-full border-2 border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 text-zinc-400 dark:text-zinc-600 font-bold text-xs flex items-center justify-center mb-6 transition-colors group-hover:border-brand dark:group-hover:border-brand-light group-hover:text-brand dark:group-hover:text-brand-light">
                            01
                        </div>
                        <h3 class="text-lg font-header font-bold text-zinc-900 dark:text-white mb-3">Contexto de la Industria</h3>
                        <div class="prose dark:prose-invert max-w-none">
                            {p1_html}
                        </div>
                    </div>
                    
                    <!-- Paso 2: El Desafío -->
                    <div class="flex flex-col items-start relative group">
                        <div class="w-8 h-8 rounded-full border-2 border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 text-zinc-400 dark:text-zinc-600 font-bold text-xs flex items-center justify-center mb-6 transition-colors group-hover:border-red-400 group-hover:text-red-400">
                            02
                        </div>
                        <h3 class="text-lg font-header font-bold text-zinc-900 dark:text-white mb-3">El Dolor de Gestión</h3>
                        <div class="prose dark:prose-invert max-w-none">
                            {p2_html}
                        </div>
                    </div>
                    
                    <!-- Paso 3: La Solución con IA -->
                    <div class="flex flex-col items-start relative group">
                        <div class="w-8 h-8 rounded-full bg-brand dark:bg-brand-light text-white dark:text-zinc-950 font-bold text-xs flex items-center justify-center mb-6 shadow-md shadow-brand/10">
                            03
                        </div>
                        <h3 class="text-lg font-header font-bold text-zinc-900 dark:text-white mb-3">Solución con IA</h3>
                        <div class="w-full">
                            <h4 class="text-sm font-semibold text-brand dark:text-brand-light mb-3">{h3_text}</h4>
                            <div class="prose dark:prose-invert max-w-none">
                                {p3_html}
                            </div>
                            {wa_bubble_html}
                        </div>
                    </div>
                </div>
            </div>
            
            {p_extra_html}
        </div>
    </section>
    """
    return new_html





def format_h1(h1):
    cursor = '<span class="typewriter-cursor"></span>'
    if " para " in h1:
        parts = h1.split(" para ", 1)
        return f'{parts[0]} para <span class="text-brand dark:text-brand-light block mt-2">{parts[1]}{cursor}</span>'
    elif ":" in h1:
        parts = h1.split(":", 1)
        return f'{parts[0]}: <span class="text-brand dark:text-brand-light block mt-2">{parts[1]}{cursor}</span>'
    elif " en " in h1:
        parts = h1.split(" en ", 1)
        return f'{parts[0]} en <span class="text-brand dark:text-brand-light block mt-2">{parts[1]}{cursor}</span>'
    else:
        return f'<span class="text-brand">{h1}{cursor}</span>'

def build():
    setup_dist()
    
    # Cargar caché de autocompletado
    CACHE_FILE = "data/autocomplete_cache.json"
    autocomplete_cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                autocomplete_cache = json.load(f)
            print(f"Caché de Autocomplete cargada: {len(autocomplete_cache)} registros.")
        except Exception as e:
            print(f"Error al cargar caché de autocompletado: {e}")
            
    with open(os.path.join(SRC_DIR, "template.html"), "r", encoding="utf-8") as f:
        template_html = f.read()
        
    # Read CSV
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)
        footer_html = build_footer_html(data)
        
    mega_menu_html = get_mega_menu(data)
    urls = []
    
    for row in data:
        if row.get('Estado') != 'PUBLICAR':
            continue
            
        out_html = template_html
        
        # Pre-process complex fields
        servicios_html = build_servicios_cards(row)
        faqs_html, schema_faq = build_faqs(row, autocomplete_cache)
        hermanas_html = build_ciudades_hermanas(row, data)
        wa_mensaje = row.get('WA_Mensaje_Precargado', '')
        wa_encoded = quote(wa_mensaje)
        barrios_list = row.get('Barrios', '').split('|')
        barrio_principal = barrios_list[0] if barrios_list else ''
        
        # New Dynamic SEO fields
        roadmap_html = build_roadmap_html(row)
        roi_table_html = build_roi_table_html(row)
        calculadora_roi_html = build_calculadora_html(row)
        local_context = build_local_context(row)
        
        # Spin intro paragraphs
        ciudad = row.get('Ciudad', '')
        dolor = row.get('Dolor_Principal', '')
        intro_template = INDUSTRY_DATA.get(row.get('Industria'), {}).get('intro', f"Implementamos asistentes virtuales 24/7 en WhatsApp que <strong>entienden audios, responden con empatía</strong> y resuelven <strong>{dolor}</strong>. {{Aumenta tus ventas|Escala tu atención|Mejora tu servicio}} y recupera tu tiempo en {ciudad}.")
        
        # Use simple string formatting since spin_text handles the rest
        intro_template = intro_template.replace('{ciudad}', ciudad).replace('{industria}', row.get('Industria_Singular', 'negocio'))
        
        # Apply jargon BEFORE spin_text so the spin options inside the jargon get processed
        intro_template = apply_jargon(intro_template, row.get('País', 'Default'))
        spin_intro = spin_text(intro_template)
        
        ind = row.get('Industria', '')
        hero_chat_user = INDUSTRY_DATA.get(ind, {}).get('chat', {}).get('user', f'{JARGON_DICT.get(row.get("País", "Default"), JARGON_DICT["Default"]).get("{greeting_user}", "{Hola}")}, necesito más información sobre sus servicios de {ind} en {ciudad}.')
        hero_chat_bot = INDUSTRY_DATA.get(ind, {}).get('chat', {}).get('bot', f'{JARGON_DICT.get(row.get("País", "Default"), JARGON_DICT["Default"]).get("{greeting_bot}", "¡Hola!")} Sí, somos especialistas en {ind}. ¿Te gustaría agendar una cita o prefieres ver nuestros precios?')

        # Apply jargon to chat
        hero_chat_user = spin_text(apply_jargon(hero_chat_user, row.get('País', 'Default')))
        hero_chat_bot = spin_text(apply_jargon(hero_chat_bot, row.get('País', 'Default')))

        # Replacements
        replacements = {
            '{FOOTER_HTML}': footer_html,
            '{HERO_CHAT_USER}': hero_chat_user,
            '{HERO_CHAT_BOT}': hero_chat_bot,
            '{SPIN_INTRO}': spin_intro,
            '{LOCAL_CONTEXT}': local_context,
            '{ROADMAP_HTML}': roadmap_html,
            '{TABLA_ROI_HTML}': roi_table_html,
            '{CALCULADORA_ROI_HTML}': calculadora_roi_html,
            '{MEGA_MENU}': mega_menu_html,
            '{SERVICIOS_CARDS}': servicios_html,
            '{FAQS_HTML}': faqs_html,
            '{SCHEMA_FAQ}': schema_faq,
            '{CIUDADES_HERMANAS_HTML}': hermanas_html,
            '{WA_NUMERO}': WA_NUMERO,
            '{WA_MENSAJE_ENCODED}': wa_encoded,
            '{BARRIO_PRINCIPAL}': barrio_principal,
            '{INDUSTRIA}': row.get('Industria', ''),
            '{INDUSTRIA_SLUG}': row.get('Industria_Slug', ''),
            '{INDUSTRIA_SINGULAR}': row.get('Industria_Singular', ''),
            '{PAIS}': row.get('País', ''),
            '{PAIS_SLUG}': row.get('País_Slug', ''),
            '{CODIGO_PAIS}': row.get('País_Slug', '')[:2], # approx
            '{CIUDAD}': row.get('Ciudad', ''),
            '{CIUDAD_SLUG}': row.get('Ciudad_Slug', ''),
            '{CONTENIDO_EEAT}': build_dynamic_eeat_html(row),
            '{DEMONIMO}': row.get('Demónimo', ''),
            '{MONEDA}': row.get('Moneda', ''),
            '{AEROPUERTO}': row.get('Aeropuerto', ''),
            '{URL_FINAL}': row.get('URL_Final', ''),
            '{H1}': row.get('H1', ''),
                '{H1_HTML}': format_h1(row.get('H1', '')),
            '{TITLE_SEO}': row.get('Title_SEO', ''),
            '{META_DESCRIPTION}': row.get('Meta_Description', ''),
            '{KEYWORD_PRINCIPAL}': row.get('Keyword_Principal', ''),
            '{KEYWORD_SECUNDARIA}': row.get('Keyword_Secundaria', ''),
            '{KEYWORD_TERCIARIA}': row.get('Keyword_Terciaria', ''),
            '{DOLOR_PRINCIPAL}': row.get('Dolor_Principal', ''),
            '{SOLUCION_CLAVE}': row.get('Solución_Clave', ''),
            '{PRECIO_BAJO}': row.get('Precio_Bajo', ''),
            '{PRECIO_MEDIO}': row.get('Precio_Medio', ''),
            '{PRECIO_ALTO}': row.get('Precio_Alto', ''),
            '{CLIENTE_NOMBRE}': row.get('Cliente_Nombre', ''),
            '{CLIENTE_NEGOCIO}': row.get('Cliente_Negocio', ''),
            '{CLIENTE_BARRIO}': row.get('Cliente_Barrio', ''),
            '{TESTIMONIALS_HTML}': build_testimonials_html(row),
            '{DEMO_INTERACTIVA_HTML}': build_demo_interactiva_html(row)
        }
        
        for k, v in replacements.items():
            out_html = out_html.replace(k, str(v))
            
        # Write to file
        url_final = row['URL_Final'].strip('/')
        output_path = os.path.join(DIST_DIR, url_final, "index.html")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(out_html)
            
        urls.append(f"https://consultor-ia.com.co/{url_final}/")
        
    # Generate Pillar Pages
    with open(os.path.join(SRC_DIR, "pillar.html"), "r", encoding="utf-8") as f:
        pillar_template = f.read()

    if os.path.exists(PILLARS_CSV):
        with open(PILLARS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            pillars_data = list(reader)

        for row in pillars_data:
            out_html = pillar_template
            slug = row.get('Slug', '').strip('/')
            content_html = build_pillar_content(row)

            kw_encoded = quote(row.get('Keyword_Principal', slug.replace('-', ' ')), safe='')
            wa_mensaje = f"Hola%2C+quiero+info+sobre+{kw_encoded.replace('%20', '+')}"
            replacements = {
                '{FOOTER_HTML}': footer_html,
                '{MEGA_MENU}': mega_menu_html,
                '{H1}': row.get('H1', ''),
                '{H1_HTML}': format_h1(row.get('H1', '')),
                '{TITLE_SEO}': row.get('Title', ''),
                '{META_DESCRIPTION}': row.get('MetaDescription', ''),
                '{CONTENT_HTML}': content_html,
                '{SLUG}': slug,
                '{WA_NUMERO}': WA_NUMERO,
                '{WA_MENSAJE_ENCODED}': wa_mensaje,
            }

            for k, v in replacements.items():
                out_html = out_html.replace(k, str(v))

            output_path = os.path.join(DIST_DIR, slug, "index.html")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(out_html)

            urls.append(f"https://consultor-ia.com.co/{slug}/")
            

    # --- Generate Hub Pages ---
    with open(os.path.join(SRC_DIR, "hub-industria.html"), "r", encoding="utf-8") as f:
        hub_ind_template = f.read()

    with open(os.path.join(SRC_DIR, "hub-pais.html"), "r", encoding="utf-8") as f:
        hub_pais_template = f.read()

    industries_tree = {}
    for row in data:
        ind_slug = row.get('Industria_Slug', '').strip('/')
        ind_name = row.get('Industria', '')
        pais_slug = row.get('País_Slug', '').strip('/')
        pais_name = row.get('País', '')
        ciudad_slug = row.get('Ciudad_Slug', '').strip('/')
        ciudad_name = row.get('Ciudad', '')
        
        if ind_slug not in industries_tree:
            industries_tree[ind_slug] = {'name': ind_name, 'paises': {}}
            
        if pais_slug not in industries_tree[ind_slug]['paises']:
            industries_tree[ind_slug]['paises'][pais_slug] = {'name': pais_name, 'ciudades': []}
            
        industries_tree[ind_slug]['paises'][pais_slug]['ciudades'].append({
            'slug': ciudad_slug,
            'name': ciudad_name
        })

    for ind_slug, ind_data in industries_tree.items():
        # Build Industry Hub
        html = hub_ind_template
        ind_name = ind_data['name']
        wa_mensaje = f"Hola%2C+quiero+info+sobre+agentes+IA+para+{quote(ind_name)}"
        ind_canonical = f"https://consultor-ia.com.co/{ind_slug}/"
        ind_description = f"Implementamos agentes de Inteligencia Artificial para {ind_name} en toda Latinoamérica. Automatiza WhatsApp, gestiona citas y aumenta tus ventas 24/7 con IA conversacional."
        ind_schema = json.dumps({
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": f"IA para {ind_name} en LATAM | Consultor IA",
            "description": ind_description,
            "url": ind_canonical,
            "breadcrumb": {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://consultor-ia.com.co/"},
                    {"@type": "ListItem", "position": 2, "name": ind_name, "item": ind_canonical}
                ]
            }
        }, ensure_ascii=False, indent=2)

        replacements = {
            '{INDUSTRIA}': ind_name,
            '{WA_NUMERO}': WA_NUMERO,
            '{WA_MENSAJE_ENCODED}': wa_mensaje,
            '{MEGA_MENU}': mega_menu_html,
            '{FOOTER_HTML}': footer_html,
            '{IND_CANONICAL}': ind_canonical,
            '{IND_DESCRIPTION}': ind_description,
            '{IND_SCHEMA}': ind_schema,
        }
        
        for k, v in replacements.items():
            html = html.replace(k, str(v))
            
        enlaces_paises = ""
        for p_slug, p_data in ind_data['paises'].items():
            p_name = p_data['name']
            enlaces_paises += f'<a href="/{ind_slug}/{p_slug}/" class="group block p-6 rounded-3xl bg-white dark:bg-zinc-900/50 backdrop-blur-sm border border-gray-200 dark:border-zinc-800 hover:border-zinc-900 dark:hover:border-white dark:hover:border-white/50 transition-all duration-500 relative"><div class="absolute inset-0 rounded-[inherit] bg-zinc-50 dark:bg-zinc-800/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div><div class="relative z-10 flex flex-col items-center text-center"><h3 class="text-xl font-bold mb-2 text-zinc-900 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light transition-colors">{p_name}</h3><span class="text-sm font-semibold text-accent flex items-center gap-1 uppercase tracking-wider opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0 transition-all duration-300">Explorar Ciudades <i class="fas fa-arrow-right text-[10px]"></i></span></div></a>\n'
        
        html = html.replace('{ENLACES_PAISES}', enlaces_paises)
        
        out_dir = os.path.join(DIST_DIR, ind_slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        urls.append(f"https://consultor-ia.com.co/{ind_slug}/")
            
        for p_slug, p_data in ind_data['paises'].items():
            # Build Pais Hub
            p_html = hub_pais_template
            p_name = p_data['name']
            pais_canonical = f"https://consultor-ia.com.co/{ind_slug}/{p_slug}/"
            pais_description = f"Agentes de IA para {ind_name} en {p_name}. Automatiza WhatsApp, reservas y ventas con Inteligencia Artificial conversacional. Atiende 24/7 sin contratar más personal."
            pais_schema = json.dumps({
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": f"IA para {ind_name} en {p_name} | Consultor IA",
                "description": pais_description,
                "url": pais_canonical,
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://consultor-ia.com.co/"},
                        {"@type": "ListItem", "position": 2, "name": ind_name, "item": ind_canonical},
                        {"@type": "ListItem", "position": 3, "name": p_name, "item": pais_canonical}
                    ]
                }
            }, ensure_ascii=False, indent=2)

            p_replacements = {
                '{INDUSTRIA}': ind_name,
                '{PAIS}': p_name,
                '{INDUSTRIA_SLUG}': ind_slug,
                '{WA_NUMERO}': WA_NUMERO,
                '{MEGA_MENU}': mega_menu_html,
                '{FOOTER_HTML}': footer_html,
                '{PAIS_CANONICAL}': pais_canonical,
                '{PAIS_DESCRIPTION}': pais_description,
                '{PAIS_SCHEMA}': pais_schema,
            }
            for k, v in p_replacements.items():
                p_html = p_html.replace(k, str(v))
            
            enlaces_ciudades = ""
            for c in p_data['ciudades']:
                c_slug = c['slug']
                c_name = c['name']
                enlaces_ciudades += f'<a href="/{ind_slug}/{p_slug}/{c_slug}/" class="block p-6 rounded-2xl bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 hover:border-zinc-900 dark:hover:border-white transition-all"><h3 class="text-xl font-bold mb-2">{c_name}</h3><span class="text-sm text-accent">Ver detalles &rarr;</span></a>\n'
                
            p_html = p_html.replace('{ENLACES_CIUDADES}', enlaces_ciudades)
            
            p_out_dir = os.path.join(DIST_DIR, ind_slug, p_slug)
            os.makedirs(p_out_dir, exist_ok=True)
            with open(os.path.join(p_out_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(p_html)
            urls.append(f"https://consultor-ia.com.co/{ind_slug}/{p_slug}/")

    # Generate Sitemap
    from datetime import date
    lastmod = date.today().isoformat()
    build_agencia_pages(data, footer_html, mega_menu_html, urls)
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += f'  <url>\n    <loc>https://consultor-ia.com.co/</loc>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n    <lastmod>{lastmod}</lastmod>\n  </url>\n'
    for url in urls:
        sitemap += f'  <url>\n    <loc>{url}</loc>\n    <changefreq>weekly</changefreq>\n    <lastmod>{lastmod}</lastmod>\n  </url>\n'
    sitemap += '</urlset>'
    
    with open(os.path.join(DIST_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
        
    # Generate robots.txt
    robots = "User-agent: *\nAllow: /\n\nSitemap: https://consultor-ia.com.co/sitemap.xml"
    with open(os.path.join(DIST_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    # Generate Homepage
    build_home_page(data)

    # Generate Legal Pages
    build_legal_pages(data)

    # Copy Assets (Favicon, etc.) to dist
    import shutil
    ASSETS_DIR = "assets"
    if os.path.exists(ASSETS_DIR):
        for item in os.listdir(ASSETS_DIR):
            s = os.path.join(ASSETS_DIR, item)
            d = os.path.join(DIST_DIR, item)
            if os.path.isfile(s) and not item.endswith('.png_source'):
                shutil.copy2(s, d)
                print(f"Copied asset: {item}")

    # Guardar caché de autocompletado al final del build
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(autocomplete_cache, f, ensure_ascii=False, indent=2)
        print(f"Caché de Autocomplete guardada: {len(autocomplete_cache)} registros.")
    except Exception as e:
        print(f"Error al guardar caché de autocompletado: {e}")

    print(f"Build complete! Generated {len(urls)} localized pages + homepage.")


def build_agencia_pages(data, footer_html, mega_menu_html, urls):
    import os
    from urllib.parse import quote
    
    with open(os.path.join(SRC_DIR, "agencia.html"), "r", encoding="utf-8") as f:
        agencia_template = f.read()
        
    ciudades_colombia = set()
    for row in data:
        if row.get('País') == 'Colombia' and row.get('Estado') == 'PUBLICAR':
            ciudades_colombia.add(row.get('Ciudad'))
            
    for ciudad in ciudades_colombia:
        # Encuentra una fila representativa de esta ciudad para usar sus variables genéricas
        row = next(r for r in data if r.get('Ciudad') == ciudad and r.get('País') == 'Colombia')
        
        ciudad_slug = row.get('Ciudad_Slug', '')
        if not ciudad_slug: continue
        
        url_final = f"/agencia-de-inteligencia-artificial-en-{ciudad_slug}"
        
        out_html = agencia_template
        
        wa_mensaje = f"Hola, busco una Agencia de IA en {ciudad}"
        wa_encoded = quote(wa_mensaje)
        
        hero_chat_user = f"Hola, quisiera saber si tienen inventario del producto X y el estado de mi envío a {ciudad}."
        hero_chat_bot = f"¡Hola! Sí tenemos stock del producto X. Tu envío actual llegará mañana en la tarde. ¿Deseas que agregue el producto X a tu pedido?"
        
        replacements = {
            '{FOOTER_HTML}': footer_html,
            '{MEGA_MENU}': mega_menu_html,
            '{HERO_CHAT_USER}': hero_chat_user,
            '{HERO_CHAT_BOT}': hero_chat_bot,
            '{H1}': f"Agencia de Inteligencia Artificial en {ciudad}",
            '{H1_HTML}': f'Agencia de <span class="text-brand dark:text-brand-light block mt-2">Inteligencia Artificial en {ciudad}<span class="typewriter-cursor"></span></span>',
            '{TITLE_SEO}': f"Agencia de Inteligencia Artificial en {ciudad} 2026 | Consultor IA",
            '{META_DESCRIPTION}': f"Tu Agencia de Inteligencia Artificial en {ciudad}. Implementamos automatizaciones, agentes virtuales y consultoría estratégica para escalar tu negocio.",
            '{CIUDAD}': ciudad,
            '{PAIS}': row.get('País', ''),
            '{CODIGO_PAIS}': row.get('Codigo_Pais', 'co'),
            '{URL_FINAL}': url_final + "/",
            '{WA_NUMERO}': '573132644262',
            '{WA_MENSAJE_ENCODED}': wa_encoded,
            '{PRECIO_BAJO}': row.get('Precio_Bajo', '800.000'),
            '{PRECIO_MEDIO}': row.get('Precio_Medio', '1.800.000'),
            '{PRECIO_ALTO}': row.get('Precio_Alto', '3.500.000'),
            '{MONEDA}': row.get('Moneda', 'COP'),
            '{TESTIMONIALS_HTML}': build_testimonials_html(row)
        }
        
        for k, v in replacements.items():
            out_html = out_html.replace(k, str(v))
            
        # Limpiar variables no reemplazadas (solo variables en mayúsculas tipo {VARIABLE})
        out_html = re.sub(r'\{[A-Z0-9_]+\}', '', out_html)
            
        page_dir = os.path.join(DIST_DIR, url_final.strip('/'))
        os.makedirs(page_dir, exist_ok=True)
        
        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(out_html)
            
        urls.append(f"https://consultor-ia.com.co{url_final}/")
        print(f"Generated Agencia page for {ciudad}")


if __name__ == "__main__":
    build()
