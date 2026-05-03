import glob
import re

html_files = glob.glob('templates/*.html')

new_cta = """        <!-- CTA Final -->
        <section class="py-24 border-t border-gray-200 dark:border-zinc-800 bg-white dark:bg-zinc-950/50 relative overflow-hidden backdrop-blur-md">
            <div class="container mx-auto px-4 max-w-3xl relative z-10 text-center">
                <h2 class="text-4xl md:text-5xl font-header font-bold mb-6 text-zinc-900 dark:text-white tracking-tight">¿Listo para transformar tu negocio?</h2>
                <p class="text-xl text-zinc-600 dark:text-zinc-400 mb-10 font-medium">Agenda una sesión de consultoría gratuita de 15 minutos y descubre cómo la IA puede automatizar tus ventas y atención.</p>
                <a href="https://wa.me/{WA_NUMERO}?text={WA_MENSAJE_ENCODED}" target="_blank" class="inline-flex items-center justify-center bg-brand text-white px-10 py-4 rounded-full font-bold text-lg hover:bg-[#1da851] hover:scale-105 transition-all duration-300 shadow-lg shadow-brand/20">
                    <i class="fab fa-whatsapp text-2xl mr-3"></i> Hablar con un Experto
                </a>
            </div>
        </section>"""

for filepath in html_files:
    with open(filepath, 'r') as file:
        content = file.read()
    
    # We replace from <!-- CTA Final --> to </section> before the Footer
    # Use re.sub to replace the block
    content = re.sub(r'<!-- CTA Final -->\s*<section.*?</section>', new_cta, content, flags=re.DOTALL)
    
    with open(filepath, 'w') as file:
        file.write(content)

print("CTA fixed")
