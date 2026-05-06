import pandas as pd
import google.generativeai as genai
import os
import time

# Cargar API Key
env_path = "/Users/anthony/Downloads/GeminiDemo/CreateIA/backend/.env"
api_key = None
with open(env_path, "r") as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=")[1].strip()

if not api_key:
    print("Error: No se encontró la API Key en", env_path)
    exit(1)

genai.configure(api_key=api_key)

# Configurar el modelo
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 1024,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.5-flash",
  generation_config=generation_config,
)

csv_path = "programatic.csv"
df = pd.read_csv(csv_path)

if 'Contenido_Editorial' not in df.columns:
    df['Contenido_Editorial'] = ""

# Filtrar las filas que no tienen contenido y que deben publicarse
mask = (df['Estado'] == 'PUBLICAR') & (df['Contenido_Editorial'].isna() | (df['Contenido_Editorial'] == ''))
indices_to_process = df[mask].index[:40]

if len(indices_to_process) == 0:
    print("¡No hay filas pendientes por generar contenido editorial!")
    exit(0)

print(f"Generando contenido para {len(indices_to_process)} filas...")

for i, idx in enumerate(indices_to_process):
    row = df.loc[idx]
    
    prompt = f"""
    Eres un experto en Copywriting SEO y B2B local para la marca "Consultor IA".
    Debes escribir de 2 a 3 párrafos (aprox. 150-250 palabras en total) de contexto súper hiper-localizado sobre la industria de {row['Industria_Singular']} en la ciudad de {row['Ciudad']}, {row['País']}.
    
    Contexto para usar sutilmente:
    - Barrios mencionados: {row['Barrios']}
    - Gentilicio local: {row['Demónimo']}
    - Dolor principal que sufren: {row['Dolor_Principal']}
    - Solución: {row['Solución_Clave']}
    
    Instrucciones estrictas:
    - Escribe con un tono "Tech-Luxury", profesional, que demuestre que sabemos de qué hablamos (E-E-A-T).
    - Menciona problemas reales y locales (ej. dinámicas del comercio en esa ciudad específica, turismo, comportamiento del consumidor local).
    - Devuelve ÚNICAMENTE el código HTML con etiquetas <p class="text-lg leading-relaxed mb-6 text-gray-2 dark:text-slate-300">...</p>. No uses <h1>, <h2> o <body>. No devuelvas markdown, solo el texto en HTML.
    - Evita frases clichés robóticas como "En el vertiginoso mundo actual". Ve directo al grano corporativo.
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace('```html', '').replace('```', '').strip()
        df.at[idx, 'Contenido_Editorial'] = text
        print(f"[{i+1}/40] Generado OK para: {row['Industria']} en {row['Ciudad']}")
        time.sleep(2) # Respetar rate limits de la API
    except Exception as e:
        print(f"[{i+1}/40] Error generando para {row['Ciudad']}: {e}")

df.to_csv(csv_path, index=False)
print("¡Lote de 40 finalizado y guardado en programatic.csv!")
