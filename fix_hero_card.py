import glob
import re

html_files = glob.glob('templates/*.html')

new_card = """                    <div class="lg:w-2/5 w-full">
                        <div class="relative group-hero">
                            
                            <!-- Authority Card (Premium Minimalist) -->
                            <div class="relative bg-white/80 dark:bg-[#0a0a0a]/80 backdrop-blur-2xl border border-gray-200 dark:border-zinc-800/80 rounded-3xl p-8 shadow-2xl overflow-hidden transition-all duration-500 hover:border-brand/30">
                                
                                <div class="relative z-10">
                                    <div class="flex items-center gap-4 mb-6">
                                        <div class="w-14 h-14 rounded-2xl bg-zinc-100 dark:bg-zinc-900/80 border border-zinc-200 dark:border-zinc-800/80 flex items-center justify-center shadow-inner">
                                            <i class="fas fa-bolt text-xl text-brand"></i>
                                        </div>
                                        <div>
                                            <h3 class="font-header font-bold text-xl text-zinc-900 dark:text-white tracking-tight">Consultor IA</h3>
                                            <p class="text-brand font-medium text-sm flex items-center"><i class="fas fa-circle text-[8px] mr-1.5 animate-pulse"></i> Sistema Activo</p>
                                        </div>
                                    </div>
                                    <p class="text-zinc-600 dark:text-zinc-400 mb-6 leading-relaxed font-medium">
                                        Más de 50 empresas en {PAIS} ya escalan sus operaciones con nuestra arquitectura de agentes.
                                    </p>
                                    <div class="bg-zinc-50 dark:bg-zinc-900/40 rounded-2xl p-4 mb-6 border border-zinc-200 dark:border-zinc-800/50">
                                        <div class="flex justify-between text-sm mb-3">
                                            <span class="text-zinc-500 dark:text-zinc-400 font-medium">Implementación:</span>
                                            <span class="font-bold text-zinc-900 dark:text-white">5-7 Días</span>
                                        </div>
                                        <div class="flex justify-between text-sm">
                                            <span class="text-zinc-500 dark:text-zinc-400 font-medium">ROI Promedio:</span>
                                            <span class="font-bold text-brand">+315%</span>
                                        </div>
                                    </div>
                                    <a href="#precios" class="w-full block text-center bg-zinc-900 dark:bg-white text-white dark:text-zinc-950 py-3.5 rounded-xl font-bold hover:bg-brand dark:hover:bg-brand hover:text-white transition-colors duration-300 shadow-lg">
                                        Ver Arquitectura
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>"""

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Replace from <div class="lg:w-2/5 w-full"> up to the end of that div (matching the 4 nested divs)
    # Since regex with nested HTML is tricky, I'll use a string replacement by finding the start and end.
    
    start_str = '<div class="lg:w-2/5 w-full">'
    # The end is right before `</div>\n                </div>\n            </div>\n        </section>\n\n        <!-- 3. Logos de Confianza -->`
    
    if start_str in content:
        start_idx = content.find(start_str)
        # Find the section end
        end_idx = content.find('</section>', start_idx)
        
        # We know the card ends just a few divs before the </section>
        # Let's extract the whole block between start_str and the end of the container
        # Actually, let's use regex with a specific stopper
        
        sub = re.sub(r'<div class="lg:w-2/5 w-full">.*?<!-- 3. Logos', new_card + '\n                </div>\n            </div>\n        </section>\n\n        <!-- 3. Logos', content, flags=re.DOTALL)
        
        with open(filepath, 'w') as file:
            file.write(sub)

print("Hero card redesigned")
