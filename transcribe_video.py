import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

def transcribe():
    load_dotenv('/Users/anthony/Downloads/GeminiDemo/CreateIA/backend/.env')
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("API key not found")
        return

    client = genai.Client(api_key=api_key)
    file_path = "Agenda tu Demo en el Calendario! entre Anthony Velasquez y Mariana - 2026_05_25 10_56 GMT-05_00 - Recording.mp4"
    print(f"Subiendo {file_path}...")
    uploaded_file = client.files.upload(file=file_path)
    
    print(f"Archivo subido como {uploaded_file.name}. Esperando procesamiento...")
    
    # Wait for the file to be processed
    while True:
        file_info = client.files.get(name=uploaded_file.name)
        if file_info.state == 'ACTIVE':
            break
        elif file_info.state == 'FAILED':
            print("El procesamiento del video falló.")
            return
        time.sleep(10)
    
    print("Video listo. Iniciando transcripción con Gemini (esto puede tomar un momento)...")
    prompt = "Por favor, transcribe toda la conversación de este video de forma precisa, identificando a los hablantes (Anthony y Mariana) si es posible. Escribe la transcripción en formato Markdown y en español."
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[uploaded_file, prompt]
        )
        
        with open("transcripcion.md", "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print("¡Éxito! Transcripción guardada en transcripcion.md")
    except Exception as e:
        print(f"Error durante la generación: {e}")

if __name__ == "__main__":
    transcribe()
