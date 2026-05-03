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
                        <li class="flex items-center"><i class="fas fa-heart text-brand dark:text-white text-xl mr-3"></i> Tono conversacional y cálido</li>
                        <li class="flex items-center"><i class="fas fa-microphone text-brand dark:text-white text-xl mr-3"></i> Transcribe y entiende audios</li>
                        <li class="flex items-center"><i class="fas fa-spell-check text-brand dark:text-white text-xl mr-3"></i> Tolera jergas y errores al escribir</li>
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
                <p class="text-xl text-gray-2 dark:text-slate-400">Lanzamos tu agente de IA en 4 pasos simples, sin que tengas que programar nada.</p>
            </div>
            
            <div class="relative">
                <!-- Línea conectora -->
                <div class="absolute left-1/2 top-0 bottom-0 w-px bg-accent/30 dark:bg-accent/20 -translate-x-1/2"></div>
                
                <div class="space-y-8 md:space-y-12">
                    <!-- Paso 1 -->
                    <div class="relative flex flex-col md:flex-row items-center md:justify-between group pt-16 md:pt-0">
                        <div class="md:w-5/12 text-center md:text-right pr-0 md:pr-12">
                            <h3 class="text-2xl font-header font-bold mb-3 text-gray-1 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light transition-colors">1. Auditoría y Estrategia</h3>
                            <p class="text-gray-500 dark:text-slate-400">Analizamos el flujo de ventas de tu {industria} y definimos la personalidad y base de conocimiento del agente.</p>
                        </div>
                        <div class="absolute top-0 md:top-1/2 md:-translate-y-1/2 left-1/2 -translate-x-1/2 w-12 h-12 rounded-full bg-[#FDFBF7] dark:bg-zinc-900 border-4 border-brand dark:border-white/20 flex items-center justify-center font-bold text-brand dark:text-white shadow-[0_0_15px_rgba(226,125,96,0.3)] dark:shadow-none z-10">1</div>
                        <div class="md:w-5/12 pl-0 md:pl-12 hidden md:block"></div>
                    </div>
                    
                    <!-- Paso 2 -->
                    <div class="relative flex flex-col md:flex-row items-center md:justify-between group pt-16 md:pt-0">
                        <div class="md:w-5/12 pr-0 md:pr-12 hidden md:block"></div>
                        <div class="absolute top-0 md:top-1/2 md:-translate-y-1/2 left-1/2 -translate-x-1/2 w-12 h-12 rounded-full bg-[#FDFBF7] dark:bg-zinc-900 border-4 border-brand dark:border-white/20 flex items-center justify-center font-bold text-brand dark:text-white shadow-[0_0_15px_rgba(226,125,96,0.3)] dark:shadow-none z-10">2</div>
                        <div class="md:w-5/12 pl-0 md:pl-12 text-center md:text-left">
                            <h3 class="text-2xl font-header font-bold mb-3 text-gray-1 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light transition-colors">2. Entrenamiento IA</h3>
                            <p class="text-gray-500 dark:text-slate-400">Cargamos tus PDFs, FAQs e historial de WhatsApp para que la IA responda como tu mejor vendedor.</p>
                        </div>
                    </div>
                    
                    <!-- Paso 3 -->
                    <div class="relative flex flex-col md:flex-row items-center md:justify-between group pt-16 md:pt-0">
                        <div class="md:w-5/12 text-center md:text-right pr-0 md:pr-12">
                            <h3 class="text-2xl font-header font-bold mb-3 text-gray-1 dark:text-white group-hover:text-brand dark:group-hover:text-brand-light transition-colors">3. Integración WhatsApp</h3>
                            <p class="text-gray-500 dark:text-slate-400">Conectamos el cerebro de IA con el número de WhatsApp oficial de tu negocio de forma segura.</p>
                        </div>
                        <div class="absolute top-0 md:top-1/2 md:-translate-y-1/2 left-1/2 -translate-x-1/2 w-12 h-12 rounded-full bg-[#FDFBF7] dark:bg-zinc-900 border-4 border-brand dark:border-white/20 flex items-center justify-center font-bold text-brand dark:text-white shadow-[0_0_15px_rgba(226,125,96,0.3)] dark:shadow-none z-10">3</div>
                        <div class="md:w-5/12 pl-0 md:pl-12 hidden md:block"></div>
                    </div>
                    
                    <!-- Paso 4 -->
                    <div class="relative flex flex-col md:flex-row items-center md:justify-between group pt-16 md:pt-0">
                        <div class="md:w-5/12 pr-0 md:pr-12 hidden md:block"></div>
                        <div class="absolute top-0 md:top-1/2 md:-translate-y-1/2 left-1/2 -translate-x-1/2 w-12 h-12 rounded-full bg-brand dark:bg-zinc-800 border-4 border-brand dark:border-white/20 flex items-center justify-center font-bold text-white shadow-[0_0_20px_rgba(226,125,96,0.6)] dark:shadow-none z-10">4</div>
                        <div class="md:w-5/12 pl-0 md:pl-12 text-center md:text-left">
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
            
            <div class="bg-[#FDFBF7] dark:bg-zinc-900 border border-gray-border dark:border-zinc-800 rounded-3xl p-8 shadow-xl flex flex-col md:flex-row gap-12">
                
                <!-- Controles -->
                <div class="w-full md:w-1/2 flex flex-col justify-center space-y-8">
                    <div>
                        <div class="flex justify-between mb-2">
                            <label class="font-bold text-gray-700 dark:text-slate-300">Chats diarios recibidos</label>
                            <span id="calc-chats-val" class="text-brand font-bold">50</span>
                        </div>
                        <input type="range" id="calc-chats" min="10" max="500" value="50" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-zinc-700 accent-brand">
                        <p class="text-xs text-gray-400 mt-2">Mensajes de WhatsApp por día</p>
                    </div>
                    
                    <div>
                        <div class="flex justify-between mb-2">
                            <label class="font-bold text-gray-700 dark:text-slate-300">Ticket promedio de venta</label>
                            <span id="calc-ticket-val" class="text-brand font-bold">{moneda} 100</span>
                        </div>
                        <input type="range" id="calc-ticket" min="10" max="1000" step="10" value="100" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-zinc-700 accent-brand">
                        <p class="text-xs text-gray-400 mt-2">Valor promedio de lo que vendes</p>
                    </div>
                </div>
                
                <!-- Resultados -->
                <div class="w-full md:w-1/2 bg-white dark:bg-zinc-950 border border-gray-100 dark:border-zinc-800 rounded-2xl p-6 flex flex-col justify-center space-y-6">
                    <div class="text-center">
                        <p class="text-sm text-gray-500 dark:text-slate-400 mb-1">Horas operativas ahorradas al mes</p>
                        <div class="text-4xl font-bold text-gray-800 dark:text-white" id="res-hours">125h</div>
                    </div>
                    
                    <div class="h-px bg-gray-100 dark:bg-zinc-800 w-full"></div>
                    
                    <div class="text-center">
                        <p class="text-sm text-gray-500 dark:text-slate-400 mb-1">Leads recuperados al mes (Est. 20%)</p>
                        <div class="text-3xl font-bold text-gray-800 dark:text-white" id="res-leads">300</div>
                    </div>
                    
                    <div class="h-px bg-gray-100 dark:bg-zinc-800 w-full"></div>
                    
                    <div class="text-center bg-brand/5 dark:bg-brand/10 rounded-xl p-4 border border-brand/20">
                        <p class="text-sm text-brand dark:text-brand-light font-bold mb-1">Ingresos Extra Estimados (Mes)</p>
                        <div class="text-4xl font-bold text-brand dark:text-brand-light" id="res-revenue">{moneda} 4,500</div>
                        <p class="text-[10px] text-gray-400 mt-2">*Asumiendo un cierre del 15% sobre leads recuperados.</p>
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
            
    # Obtener ciudades principales (agrupar por país)
    countries = {}
    for row in data:
        if row.get('Estado') != 'PUBLICAR': continue
        pais = row.get('País')
        ciudad = row.get('Ciudad')
        url = row.get('URL_Final')
        if pais and ciudad and url:
            if pais not in countries:
                countries[pais] = []
            if len(countries[pais]) < 8: # Limitar a 8 ciudades por país
                countries[pais].append((ciudad, url))

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
                    <span class="font-header font-extrabold tracking-tighter text-3xl text-zinc-900 dark:text-white">Consultor-<span class="text-accent">IA</span></span>
                </a>
                <p class="text-gray-2 dark:text-slate-400 text-sm leading-relaxed">
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
                <ul class="space-y-3 text-sm text-gray-2 dark:text-slate-400">
                    {ind_links}
                </ul>
            </div>

            <!-- Col 3 & 4: Ciudades -->
            <div class="lg:col-span-2">
                <h4 class="font-header font-bold text-zinc-900 dark:text-white text-lg mb-6">Presencia en LATAM</h4>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-8 text-sm text-gray-2 dark:text-slate-400">
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
                <a href="#" class="hover:text-zinc-900 dark:hover:text-white transition-colors">Aviso Legal</a>
                <a href="#" class="hover:text-zinc-900 dark:hover:text-white transition-colors">Política de Privacidad</a>
            </div>
        </div>
    </div>
</footer>
'''
    return footer.replace("{{WA_NUMERO}}", str(WA_NUMERO))
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
        <a href="{url}" class="group flex flex-col items-center gap-3 p-6 rounded-3xl border border-gray-border dark:border-zinc-800 bg-white dark:bg-zinc-900 hover:shadow-xl hover:border-accent/30 transition-all duration-300 text-center">
            <div class="w-14 h-14 rounded-2xl bg-brand/10 dark:bg-white/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                <i class="fas {icon} text-2xl text-brand dark:text-brand-light"></i>
            </div>
            <span class="text-sm font-semibold text-zinc-800 dark:text-zinc-100 group-hover:text-brand dark:group-hover:text-brand-light transition-colors">{ind}</span>
        </a>"""

    steps_data = [
        ("fa-search", "1. Diagnóstico", "Analizamos tu negocio, flujos de atención y dónde estás perdiendo clientes."),
        ("fa-brain", "2. Entrenamiento IA", "Cargamos tu información para que la IA responda como tu mejor vendedor."),
        ("fa-rocket", "3. Lanzamiento", "Activamos el agente en tu WhatsApp oficial con monitoreo en tiempo real."),
    ]
    steps_html = ""
    for icon, title, desc in steps_data:
        steps_html += f"""
        <div class="bg-[#FDFBF7] dark:bg-zinc-900 border border-gray-border dark:border-zinc-800 rounded-3xl p-8 hover:shadow-xl transition-all duration-300 group">
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
    <link rel="icon" type="image/png" href="/favicon.png">
    <title>Consultor IA | Agentes de Inteligencia Artificial para tu Negocio en LATAM</title>
    <meta name="description" content="Automatiza la atencion al cliente, ventas y reservas con Agentes IA para WhatsApp 24/7. Para restaurantes, clinicas, hoteles y mas en LATAM.">
    <link rel="canonical" href="https://consultor-ia.com.co/">
    <meta property="og:title" content="Consultor IA | Agentes IA para Negocios LATAM">
    <meta property="og:description" content="Implementamos Agentes de Inteligencia Artificial en WhatsApp para negocios en LATAM.">
    <meta property="og:url" content="https://consultor-ia.com.co/">
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
                        'accent': '#4f46e5',
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
    </style>
</head>
<body class="bg-white dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 transition-colors duration-300">

<!-- HEADER -->
<header class="fixed top-4 inset-x-0 z-[100] flex justify-center px-4 pointer-events-none">
    <div class="w-full max-w-7xl glass rounded-full border border-gray-200 dark:border-zinc-800/80 shadow-2xl pointer-events-auto flex justify-between items-center px-6 py-3">
        <a href="/" class="flex items-center gap-2">
            <span class="font-header font-extrabold tracking-tighter text-3xl text-zinc-900 dark:text-white">Consultor-<span class="text-brand dark:text-brand-light">IA</span></span>
        </a>
        <nav class="hidden md:flex space-x-8 items-center">
            <a href="#como-funciona" class="font-medium text-gray-2 dark:text-slate-300 hover:text-brand dark:hover:text-brand-light transition-colors">Como Funciona</a>
            <a href="#industrias" class="font-medium text-gray-2 dark:text-slate-300 hover:text-brand dark:hover:text-brand-light transition-colors">Industrias</a>
            <a href="/blog/" class="font-medium text-gray-2 dark:text-slate-300 hover:text-brand dark:hover:text-brand-light transition-colors">Blog</a>
            <button id="theme-toggle" class="text-gray-500 dark:text-slate-400 hover:text-brand focus:outline-none rounded-lg text-lg p-2.5 transition-colors">
                <i id="theme-toggle-dark-icon" class="fas fa-moon hidden"></i>
                <i id="theme-toggle-light-icon" class="fas fa-sun hidden"></i>
            </button>
            <a href="https://wa.me/WA_NUM?text=Hola%2C+quiero+una+demo+del+agente+IA" target="_blank" class="group relative inline-flex items-center justify-center border border-zinc-900 dark:border-white px-6 py-2 overflow-hidden transition-all duration-500">
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
                <p class="text-xl text-gray-2 dark:text-slate-300 mb-10 leading-relaxed max-w-2xl">
                    Implementamos <strong>Agentes de Inteligencia Artificial</strong> en WhatsApp que responden, agendan y venden por ti. Sin contratar mas personal. Sin perder un solo cliente.
                </p>
                <div class="flex flex-col sm:flex-row gap-4 mb-12">
                    <a href="https://wa.me/WA_NUM?text=Hola%2C+quiero+una+demo+del+agente+IA" target="_blank" class="group relative inline-flex items-center justify-center border border-zinc-900 dark:border-white px-8 py-4 overflow-hidden transition-all duration-500">
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
            <p class="text-xl text-gray-2 dark:text-slate-400">Sin codigo, sin complicaciones. Nosotros hacemos todo el trabajo tecnico.</p>
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
            <p class="text-xl text-gray-2 dark:text-slate-400">Cada agente es entrenado con el lenguaje y procesos especificos de tu sector.</p>
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
        <p class="text-xl text-gray-2 dark:text-slate-400 mb-10 max-w-2xl mx-auto">Unete a los negocios de LATAM que ya atienden, agendan y venden en piloto automatico.</p>
        <a href="https://wa.me/WA_NUM?text=Hola%2C+quiero+una+demo+del+agente+IA" target="_blank" class="group relative inline-flex items-center justify-center border border-zinc-900 dark:border-white px-10 py-5 overflow-hidden transition-all duration-500">
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
            <button id="close-menu-btn" class="text-3xl text-zinc-900 dark:text-white focus:outline-none">
                <i class="fas fa-times"></i>
            </button>
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
    if (document.documentElement.classList.contains('dark')) {{ themeToggleLightIcon.classList.remove('hidden'); }} else {{ themeToggleDarkIcon.classList.remove('hidden'); }}
    themeToggleBtn.addEventListener('click', function() {{
        themeToggleDarkIcon.classList.toggle('hidden');
        themeToggleLightIcon.classList.toggle('hidden');
        if (document.documentElement.classList.contains('dark')) {{
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }} else {{
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }}
    }});

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

    html = html.replace('WA_NUM', WA_NUMERO)

    output_path = os.path.join(DIST_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path

def setup_dist():

    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)
    else:
        # Delete everything inside DIST_DIR except .git
        for filename in os.listdir(DIST_DIR):
            if filename not in ['.git', 'Dosckerfile', 'Dockerfile']:
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
        <div class="bg-[#FDFBF7] dark:bg-zinc-900 border border-gray-border dark:border-zinc-800 rounded-3xl p-8 hover:shadow-xl transition-all duration-300 group">
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
            
            # Simple content list based on priority (placeholder logic)
            content_html = f'<div class="p-4 bg-gray-50 dark:bg-slate-800 rounded-xl border border-gray-border dark:border-slate-700"><h3 class="font-bold text-brand dark:text-brand-light">{row.get("H1")}</h3><p class="text-sm mt-2 text-gray-600 dark:text-slate-400">Contenido en desarrollo para {row.get("Keyword_Principal")}.</p></div>'
            
            replacements = {
                '{FOOTER_HTML}': footer_html,
                '{H1}': row.get('H1', ''),
                '{H1_HTML}': format_h1(row.get('H1', '')),
                '{TITLE_SEO}': row.get('Title', ''),
                '{META_DESCRIPTION}': row.get('MetaDescription', ''),
                '{CONTENT_HTML}': content_html
            }
            
            for k, v in replacements.items():
                out_html = out_html.replace(k, str(v))
                
            output_path = os.path.join(DIST_DIR, slug, "index.html")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(out_html)
                
            urls.append(f"https://consultor-ia.com.co/{slug}/")
            
    # Generate Sitemap
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap += f'  <url>\n    <loc>{url}</loc>\n    <changefreq>weekly</changefreq>\n  </url>\n'
    sitemap += '</urlset>'
    
    with open(os.path.join(DIST_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
        
    # Generate robots.txt
    robots = "User-agent: *\nAllow: /\n\nSitemap: https://consultor-ia.com.co/sitemap.xml"
    with open(os.path.join(DIST_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    # Generate Homepage
    build_home_page(data)

    print(f"Build complete! Generated {len(urls)} localized pages + homepage.")

if __name__ == "__main__":
    build()
