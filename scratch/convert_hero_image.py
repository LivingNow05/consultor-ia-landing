from PIL import Image
import os

src = "/Users/anthony/.gemini/antigravity/brain/81f1b6de-28a6-4206-95da-c7829ab6568b/hero_ia_salud_1780002390911.png"
dst = "/Users/anthony/Downloads/consultor-ia.com.co/images/blog/ia-para-salud/hero.webp"

if os.path.exists(src):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    img = Image.open(src)
    img.save(dst, "WEBP", quality=90)
    print(f"✅ Conversión completada: {src} -> {dst}")
else:
    print(f"❌ Error: No se encontró la imagen de origen en {src}")
