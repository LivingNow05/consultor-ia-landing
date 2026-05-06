import os
import glob
from PIL import Image

output_dir = "images/"
dist_dir = "dist/images/"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(dist_dir, exist_ok=True)

# Find all new AI sketch PNGs
sketches = glob.glob("/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/*_ai_sketch_*.png")

# Mapping rules
name_mapping = {
    "restaurantes": "og-restaurantes.webp",
    "salones_belleza": "og-salones-de-belleza.webp",
    "clinicas_dentales": "og-clinicas-dentales.webp",
    "inmobiliarias": "og-inmobiliarias.webp",
    "gimnasios": "og-gimnasios.webp",
    "hoteles_hostales": "og-hoteles-y-hostales.webp",
    "clinicas_veterinarias": "og-clinicas-veterinarias.webp",
    "agencias_marketing": "og-agencias-de-marketing.webp",
    "estudios_abogados": "og-estudios-de-abogados.webp",
    "instituciones_educativas": "og-instituciones-educativas.webp"
}

for sketch in sketches:
    filename = os.path.basename(sketch)
    # identify prefix
    for key, val in name_mapping.items():
        if filename.startswith(key):
            try:
                img = Image.open(sketch)
                img = img.convert("RGB")
                img.save(os.path.join(output_dir, val), "WEBP", quality=80)
                img.save(os.path.join(dist_dir, val), "WEBP", quality=80)
                print(f"Updated {val} with new AI diagram sketch.")
            except Exception as e:
                print(f"Error processing {sketch}: {e}")
            break

