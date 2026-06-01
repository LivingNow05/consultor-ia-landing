import os
from PIL import Image

src_png = "/Users/anthony/.gemini/antigravity/brain/72398725-1f18-40b4-a973-5dba68b63e95/hotel_chatbot_hero_1780347996418.png"
dst_dir = "/Users/anthony/Downloads/consultor-ia.com.co/images/blog/ia-para-hoteles"
dst_webp = os.path.join(dst_dir, "hero.webp")

os.makedirs(dst_dir, exist_ok=True)
img = Image.open(src_png)
# Redimensionar si es necesario para optimizar peso (por ejemplo, máx 1200px de ancho)
img.thumbnail((1200, 1200))
img.save(dst_webp, "WEBP", quality=85)
print(f"Saved optimized webp image to {dst_webp}")
