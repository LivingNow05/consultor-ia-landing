import os
import glob
from PIL import Image

slugs = {
    'restaurantes': 'restaurantes',
    'salones_belleza': 'salones-de-belleza',
    'clinicas_dentales': 'clinicas-dentales',
    'inmobiliarias': 'inmobiliarias',
    'gimnasios': 'gimnasios',
    'hoteles_hostales': 'hoteles-y-hostales',
    'clinicas_veterinarias': 'clinicas-veterinarias',
    'agencias_marketing': 'agencias-de-marketing',
    'estudios_abogados': 'estudios-de-abogados',
    'instituciones_educativas': 'instituciones-educativas'
}

artifact_dir = "/Users/anthony/.gemini/antigravity/brain/55acae4e-3da3-4c80-aa4d-5b5e559ab950/"

for prefix, slug in slugs.items():
    files = glob.glob(os.path.join(artifact_dir, f"{prefix}_*.png"))
    if files:
        latest_file = sorted(files)[-1]
        out_path = f"images/og-{slug}.webp"
        print(f"Converting {latest_file} to {out_path}...")
        img = Image.open(latest_file)
        img.save(out_path, "WEBP", quality=85)
        print(f"Saved {out_path}")
    else:
        print(f"No file found for {prefix}")
