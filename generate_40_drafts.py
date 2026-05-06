import pandas as pd
import google.generativeai as genai
import time
import os

env_path = "/Users/anthony/Downloads/GeminiDemo/CreateIA/backend/.env"
api_key = None
with open(env_path, "r") as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=")[1].strip()

genai.configure(api_key=api_key)

generation_config = {
  "temperature": 0.7,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
)

df = pd.read_csv('programatic.csv')

prompt_template = """
Actúa como un experto en SEO Local y Consultor de Inteligencia Artificial Empresarial (E-E-A-T).
Escribe un texto editorial único y profundo (aprox 200-300 palabras) para una landing page B2B enfocada en vender automatización y agentes de IA.

Ciudad: {ciudad}
Industria: {industria}
Problema típico: {problema}

El texto debe:
1. Demostrar experiencia real mencionando dinámicas de la industria '{industria}' en '{ciudad}'.
2. Explicar claramente cómo la IA resuelve el '{problema}'.
3. Usar un tono ejecutivo, directo y persuasivo.
4. Formatearlo en HTML simple (usando etiquetas <p>, <strong>, y listas si aplica, pero SIN etiqueta <h1> ni <section>).
5. Asegurar que sea 100% único, no genérico.
"""

output_md = "/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/borradores_40.md"
with open(output_md, "w") as f:
    f.write("# Borradores de Contenido Editorial (Primeros 40)\n\n")

for idx, row in df.head(40).iterrows():
    ciudad = row['Ciudad']
    industria = row['Industria']
    problema = row['Dolor_Principal']
    
    prompt = prompt_template.format(ciudad=ciudad, industria=industria, problema=problema)
    print(f"Generando {idx+1}/40: {industria} en {ciudad}...")
    
    success = False
    retries = 0
    while not success and retries < 3:
        try:
            response = model.generate_content(prompt)
            texto = response.text
            
            with open(output_md, "a") as f:
                f.write(f"## {idx+1}. {industria} en {ciudad}\n\n")
                f.write(f"**Problema:** {problema}\n\n")
                f.write(f"```html\n{texto}\n```\n\n---\n\n")
                
            success = True
            time.sleep(15) # Stay under 15 RPM free tier limit
        except Exception as e:
            print(f"Error: {e}. Retrying in 30s...")
            time.sleep(30)
            retries += 1

print("Done!")
