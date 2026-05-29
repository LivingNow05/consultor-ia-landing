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

def build_chat_simulation_html(row):
    industria = row.get('Industria_Slug', '').lower()
    
    # Textos por defecto
    user_msg = "hola q tal una pregutna, cm funciona su servicio?"
    bot_msg = "Hola, un gusto saludarte. Nuestro servicio es súper sencillo de usar. Cuéntame un poquito sobre tu negocio y te explico cómo te podemos ayudar."
    
    # Personalización simple basada en industria
    if 'odontolog' in industria or 'dental' in industria or 'salud' in industria:
        user_msg = "hola, a q hr tienen cita para mañan? nesesito algo urgente xq me duele mucho la muela"
        bot_msg = "Hola, lamento mucho que te duela la muela. Mañana empezamos a atender a las 8 am. Si te parece bien, te puedo hacer un espacio a esa hora para que te vea el doctor de urgencia. ¿Me dices tu nombre para anotarte?"
    elif 'gimnasio' in industria or 'crossfit' in industria or 'fitness' in industria:
        user_msg = "ola q precio tiene el mes? y a q hora abren en la mañna"
        bot_msg = "Hola, ¿cómo estás? El mes completo está en promoción. Abrimos desde las 5 am para que vengas a entrenar temprano. ¿Te gustaría que te mande los detalles de los planes o prefieres venir a conocer el lugar primero?"
    elif 'inmobiliaria' in industria or 'bienes-raices' in industria or 'bienes raices' in industria:
        user_msg = "hola tngo un depto para alquilar en el centro, usd se encargan d tdo?"
        bot_msg = "Hola, sí claro. Nosotros nos encargamos de todo el proceso para que no te preocupes por nada. Tomamos las fotos, hacemos los contratos y filtramos a los inquilinos. ¿Te parece si me cuentas un poco más del apartamento?"
    elif 'restaurante' in industria or 'comida' in industria:
        user_msg = "holas a q hora cierran? kiero hacer un pedido para 5 personas"
        bot_msg = "Hola, cerramos a las 11 pm, así que estás a muy buen tiempo. Te puedo tomar el pedido para las 5 personas por aquí mismo. ¿Te comparto nuestro menú para que lo revises?"
    elif 'belleza' in industria or 'spa' in industria or 'peluqueria' in industria:
        user_msg = "hola tenen cita para uñas hoy? esq me urge para un evento en la noxe"
        bot_msg = "Hola, entiendo que te urge. Déjame revisar la agenda... Sí, tengo un espacio libre a las 4 pm con nuestra mejor especialista. ¿Te lo reservo de una vez para que quedes lista para tu evento?"

    html = f'''
    <section class="py-24 bg-[#FDFBF7] dark:bg-zinc-900 border-y border-gray-100 dark:border-zinc-800 relative overflow-hidden">
        <!-- Decoration -->
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-accent/5 rounded-full blur-3xl -z-10"></div>
        
        <div class="container mx-auto px-4 max-w-5xl">
            <div class="flex flex-col lg:flex-row items-center gap-16">
                <!-- Text Area -->
                <div class="lg:w-1/2 text-center lg:text-left">
                    <span class="text-brand dark:text-brand-light font-normal tracking-wider uppercase text-sm mb-2 block">La Gran Diferencia</span>
                    <h2 class="text-3xl md:text-5xl font-header font-bold mb-6">No parecemos un bot de menú aburrido</h2>
                    <p class="text-xl text-gray-500 dark:text-slate-400 mb-8">Tus clientes odian presionar el "1" para ventas o el "2" para soporte. Nuestro agente interactúa de forma natural: <strong>entiende notas de voz, perdona faltas de ortografía y responde con empatía.</strong></p>
                    <ul class="space-y-4 text-left inline-block lg:block mx-auto text-gray-700 dark:text-slate-300 font-medium">
                        <li class="flex items-center"><i class="fas fa-heart text-brand dark:text-brand-light dark:text-white text-xl mr-3"></i> Tono conversacional y cálido</li>
                        <li class="flex items-center"><i class="fas fa-microphone text-brand dark:text-brand-light dark:text-white text-xl mr-3"></i> Transcribe y entiende audios</li>
                        <li class="flex items-center"><i class="fas fa-spell-check text-brand dark:text-brand-light dark:text-white text-xl mr-3"></i> Tolera jergas y errores al escribir</li>
                    </ul>
                </div>
                
                <!-- Chat Simulation Area -->
                <div class="lg:w-1/2 w-full max-w-md mx-auto relative group">
                    <div class="absolute -inset-1 bg-gradient-to-r from-brand to-success rounded-[2.5rem] blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>
                    <div class="bg-[#E5DDD5] dark:bg-[#0b141a] rounded-[2rem] shadow-2xl border-[8px] border-white dark:border-zinc-800 overflow-hidden relative">
                        <!-- Chat Header -->
                        <div class="bg-[#00a884] dark:bg-[#202c33] px-6 py-4 flex items-center gap-4 relative z-10 shadow-sm">
                            <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center shrink-0">
                                <i class="fas fa-robot text-[#00a884] dark:text-[#8696a0] text-xl"></i>
                            </div>
                            <div>
                                <h4 class="text-white font-medium">Asistente IA</h4>
                                <p class="text-white/80 text-xs">en línea</p>
                            </div>
                        </div>
                        
                        <!-- Chat Body -->
                        <div class="h-80 overflow-y-auto p-4 flex flex-col gap-4 relative" id="demo-chat-container">
                            <!-- Background Pattern -->
                            <div class="absolute inset-0 opacity-[0.15] dark:opacity-[0.03] bg-[url('https://i.pinimg.com/736x/8c/98/99/8c98994518b575bfd8c949e91d20548b.jpg')] bg-cover bg-center pointer-events-none z-0"></div>
                            
                            <!-- Static Messages -->
                            <div class="relative z-10 max-w-[85%] self-end bg-[#dcf8c6] dark:bg-[#005c4b] text-gray-800 dark:text-[#e9edef] px-4 py-2.5 rounded-2xl rounded-tr-none shadow-sm text-[15px] leading-snug">
                                {user_msg}
                                <span class="text-[10px] text-gray-500 dark:text-gray-400 float-right mt-2 ml-3">10:42 <i class="fas fa-check-double text-blue-500"></i></span>
                            </div>
                            
                            <div class="relative z-10 max-w-[85%] self-start bg-white dark:bg-[#202c33] text-gray-800 dark:text-[#e9edef] px-4 py-2.5 rounded-2xl rounded-tl-none shadow-sm text-[15px] leading-snug border border-gray-100 dark:border-zinc-800 mt-2">
                                {bot_msg}
                                <span class="text-[10px] text-gray-400 float-right mt-2 ml-3">10:42</span>
                            </div>
                        </div>
                        
                        <!-- Chat Input -->
                        <div class="bg-[#f0f2f5] dark:bg-[#202c33] px-4 py-3 flex items-center gap-3 relative z-10 border-t border-gray-200 dark:border-zinc-800">
                            <i class="far fa-smile text-gray-500 dark:text-[#8696a0] text-xl"></i>
                            <div class="flex-1 bg-white dark:bg-[#2a3942] rounded-full px-4 py-2 flex items-center shadow-sm">
                                <input type="text" placeholder="Escribe un mensaje aquí..." class="w-full bg-transparent border-none focus:outline-none text-gray-700 dark:text-[#e9edef] text-[15px]" onkeypress="if(event.key === 'Enter') window.sendDemoChat(this)">
                            </div>
                            <button onclick="window.sendDemoChat(this.previousElementSibling.querySelector('input'))" class="w-10 h-10 rounded-full bg-[#00a884] flex items-center justify-center text-white hover:bg-[#008f6f] transition-colors shadow-sm">
                                <i class="fas fa-paper-plane text-sm ml-0.5"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            window.sendDemoChat = function(inputEl) {{
                const msg = inputEl.value.trim();
                if(!msg) return;
                
                // Find the closest chat container
                const container = inputEl.closest('.group').querySelector('#demo-chat-container');
                
                // User Message
                const userDiv = document.createElement('div');
                userDiv.className = 'relative z-10 max-w-[85%] self-end bg-[#dcf8c6] dark:bg-[#005c4b] text-gray-800 dark:text-[#e9edef] px-4 py-2.5 rounded-2xl rounded-tr-none shadow-sm text-[15px] leading-snug animate-fade-in-up demo-user-msg';
                userDiv.innerHTML = msg + '<span class="text-[10px] text-gray-500 dark:text-gray-400 float-right mt-2 ml-3">Ahora <i class="fas fa-check text-gray-400 demo-ticks"></i></span>';
                container.appendChild(userDiv);
                
                inputEl.value = '';
                container.scrollTop = container.scrollHeight;
                
                // Typing Indicator
                const typingDiv = document.createElement('div');
                typingDiv.className = 'relative z-10 max-w-[85%] self-start bg-white dark:bg-[#202c33] text-gray-800 dark:text-[#e9edef] px-4 py-4 rounded-2xl rounded-tl-none shadow-sm border border-gray-100 dark:border-zinc-800 mt-2 flex items-center gap-1.5';
                typingDiv.innerHTML = '<span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></span><span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></span><span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>';
                container.appendChild(typingDiv);
                container.scrollTop = container.scrollHeight;
                
                setTimeout(() => {{
                    container.removeChild(typingDiv);
                    
                    const botDiv = document.createElement('div');
                    botDiv.className = 'relative z-10 max-w-[85%] self-start bg-white dark:bg-[#202c33] text-gray-800 dark:text-[#e9edef] px-4 py-2.5 rounded-2xl rounded-tl-none shadow-sm text-[15px] leading-snug border border-gray-100 dark:border-zinc-800 mt-2 animate-fade-in-up';
                    
                    let response = "¡Hola! Como soy un demo para tu {industria}, mis respuestas aquí son limitadas. ¡Pero haz clic en 'Hablar con asesor' arriba para chatear con mi versión real en WhatsApp!";
                    if(msg.toLowerCase().includes("precio") || msg.toLowerCase().includes("cuanto") || msg.toLowerCase().includes("costo") || msg.toLowerCase().includes("planes")) {{
                        response = "Nuestros planes se adaptan a negocios de {industria}. Si revisas la sección 'Precios' verás las opciones. ¿Agendamos una demo?";
                    }} else if(msg.toLowerCase().includes("gracias") || msg.toLowerCase().includes("ok") || msg.toLowerCase().includes("excelente")) {{
                        response = "¡Con gusto! Imagina a este agente atendiendo a todos los clientes de tu {industria} 24/7. ¡Pruébame en vivo!";
                    }}
                    
                    botDiv.innerHTML = response + '<span class="text-[10px] text-gray-400 float-right mt-2 ml-3">Ahora</span>';
                    container.appendChild(botDiv);
                    container.scrollTop = container.scrollHeight;
                    
                    // Update user ticks
                    const ticks = userDiv.querySelector('.demo-ticks');
                    if(ticks) ticks.className = 'fas fa-check-double text-blue-500 demo-ticks';
                    
                }}, 1500);
            }};
        </script>
    </section>
    '''
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
                            <h3 class="text-2xl font-header font-bold mb-3 text-gray-1 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light dark:hover:text-brand-light dark:group-hover:text-brand dark:group-hover:text-brand-light dark:hover:text-brand-light-light transition-colors">1. Auditoría y Estrategia</h3>
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
                            <h3 class="text-2xl font-header font-bold mb-3 text-gray-1 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light dark:hover:text-brand-light dark:group-hover:text-brand dark:group-hover:text-brand-light dark:hover:text-brand-light-light transition-colors">2. Entrenamiento IA</h3>
                            <p class="text-gray-500 dark:text-slate-400">Cargamos tus PDFs, FAQs e historial de WhatsApp para que la IA responda como tu mejor vendedor.</p>
                        </div>
                    </div>
                    
                    <!-- Paso 3 -->
                    <div class="relative flex flex-col md:flex-row items-start md:items-center md:justify-between group">
                        <div class="md:w-5/12 text-left md:text-right pl-16 md:pl-0 md:pr-12">
                            <h3 class="text-2xl font-header font-bold mb-3 text-gray-1 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light dark:hover:text-brand-light dark:group-hover:text-brand dark:group-hover:text-brand-light dark:hover:text-brand-light-light transition-colors">3. Integración WhatsApp</h3>
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
                            <h3 class="text-2xl font-header font-bold mb-3 text-gray-1 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light dark:hover:text-brand-light dark:group-hover:text-brand dark:group-hover:text-brand-light dark:hover:text-brand-light-light transition-colors">4. Lanzamiento y Optimización</h3>
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
        precio_num = float(re.sub(r'[^\d.]', '', precio_bajo))
        costo_humano_num = precio_num * 4
        costo_humano = f"{moneda} {costo_humano_num:,.0f}"
    except:
        costo_humano = f"{moneda} 400"
        
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
                            <td class="p-5 text-center font-bold text-brand dark:text-brand-light bg-brand/5 dark:bg-brand/10">Desde {precio_bajo}</td>
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
            0% {{ transform: translate(0, 0) scale(1); }}
            33% {{ transform: translate(10vw, -10vh) scale(1.1); }}
            66% {{ transform: translate(-10vw, 10vh) scale(0.9); }}
            100% {{ transform: translate(0, 0) scale(1); }}
        }}
        @keyframes global-blob-2 {{
            0% {{ transform: translate(0, 0) scale(1); }}
            33% {{ transform: translate(-10vw, 15vh) scale(1.15); }}
            66% {{ transform: translate(15vw, -10vh) scale(0.85); }}
            100% {{ transform: translate(0, 0) scale(1); }}
        }}
        @keyframes global-blob-3 {{
            0% {{ transform: translate(0, 0) scale(1); }}
            50% {{ transform: translate(10vw, 10vh) scale(1.2); }}
            100% {{ transform: translate(0, 0) scale(1); }}
        }}
        .global-blob-1 {{ animation: global-blob-1 30s infinite alternate ease-in-out; }}
        .global-blob-2 {{ animation: global-blob-2 35s infinite alternate ease-in-out; }}
        .global-blob-3 {{ animation: global-blob-3 40s infinite alternate ease-in-out; }}
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
            <a href="#como-funciona" class="font-medium text-zinc-600 dark:text-zinc-300 hover:text-brand dark:hover:text-brand dark:hover:text-brand-light-light transition-colors">Como Funciona</a>
            <a href="#industrias" class="font-medium text-zinc-600 dark:text-zinc-300 hover:text-brand dark:hover:text-brand dark:hover:text-brand-light-light transition-colors">Industrias</a>
            <a href="/blog/" class="font-medium text-zinc-600 dark:text-zinc-300 hover:text-brand dark:hover:text-brand dark:hover:text-brand-light-light transition-colors">Blog</a>
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
            <a href="/" class="hover:text-brand dark:hover:text-brand dark:hover:text-brand-light-light transition-colors">Inicio</a>
            <a href="#como-funciona" class="mobile-link hover:text-brand dark:hover:text-brand dark:hover:text-brand-light-light transition-colors">Cómo Funciona</a>
            <a href="#precios" class="mobile-link hover:text-brand dark:hover:text-brand dark:hover:text-brand-light-light transition-colors">Precios</a>
            <a href="/blog/" class="hover:text-brand dark:hover:text-brand dark:hover:text-brand-light-light transition-colors">Blog</a>
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
            if filename not in ['.git', 'Dosckerfile', 'Dockerfile', 'blog']:
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
                html += f'<li><a href="{url}" class="block py-1.5 px-3 rounded-lg text-zinc-500 dark:text-zinc-400 hover:text-brand dark:hover:text-brand dark:hover:text-brand-light-light hover:bg-brand/5 dark:hover:bg-brand/10 transition-all duration-200">{ciudad}</a></li>'
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

def build_faqs(row):
    ind = row.get('Industria', '')
    faqs = INDUSTRY_DATA.get(ind, {}).get('faqs', [])
    
    questions = [(faq['q'], faq['a']) for faq in faqs]
    # Add general FAQs from the row to bulk it up
    questions.extend([
        (row.get('FAQ_General_1_P'), row.get('FAQ_General_1_R')),
        (row.get('FAQ_General_2_P'), row.get('FAQ_General_2_R')),
        (row.get('FAQ_General_3_P'), row.get('FAQ_General_3_R'))
    ])
    
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
        faqs_html, schema_faq = build_faqs(row)
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
            '{CHAT_SIMULACION_HTML}': build_chat_simulation_html(row),
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
            '{CONTENIDO_EEAT}': row.get('Contenido_EEAT', ''),
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
            '{CLIENTE_BARRIO}': row.get('Cliente_Barrio', '')
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
            enlaces_paises += f'<a href="/{ind_slug}/{p_slug}/" class="group block p-6 rounded-3xl bg-white dark:bg-zinc-900/50 backdrop-blur-sm border border-gray-200 dark:border-zinc-800 hover:border-zinc-900 dark:hover:border-white dark:hover:border-white/50 transition-all duration-500 relative"><div class="absolute inset-0 rounded-[inherit] bg-zinc-50 dark:bg-zinc-800/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div><div class="relative z-10 flex flex-col items-center text-center"><h3 class="text-xl font-bold mb-2 text-zinc-900 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light dark:hover:text-brand-light dark:group-hover:text-brand dark:group-hover:text-brand-light dark:hover:text-brand-light-light transition-colors">{p_name}</h3><span class="text-sm font-semibold text-accent flex items-center gap-1 uppercase tracking-wider opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0 transition-all duration-300">Explorar Ciudades <i class="fas fa-arrow-right text-[10px]"></i></span></div></a>\n'
        
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
            '{MONEDA}': row.get('Moneda', 'COP')
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
