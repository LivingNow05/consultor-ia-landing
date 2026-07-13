import os
import glob
from PIL import Image

artifact_dir = "/Users/anthony/.gemini/antigravity/brain/09a899df-f4d5-4000-b660-713831804eb9"
search_pattern = os.path.join(artifact_dir, "hero_payments_whatsapp_*.jpg")
files = glob.glob(search_pattern)

if not files:
    print("Error: No se encontró la imagen generada.")
    exit(1)

latest_file = sorted(files)[-1]
print(f"Imagen de origen encontrada: {latest_file}")

dest_dir = "/Users/anthony/Downloads/consultor-ia.com.co/images/blog/pagos-en-whatsapp-chatbot"
os.makedirs(dest_dir, exist_ok=True)
dest_path = os.path.join(dest_dir, "hero.webp")

print(f"Convirtiendo a WEBP y guardando en: {dest_path}")
img = Image.open(latest_file)
img.save(dest_path, "WEBP", quality=85)
print("¡Conversión exitosa!")
