# Especificación: Sección de Recomendación de Blogs y Estrategia de Retención de Usuarios

## 1. Objetivo
El objetivo es implementar una nueva sección de recomendación de artículos del blog en la parte inferior de las páginas de destino (landings programáticas), justo debajo de la sección de "Ciudades Hermanas" ("Más Restaurantes en Colombia", etc.). Esta sección está diseñada para aumentar el tiempo de retención en página al ofrecer contenido relevante y especializado de acuerdo a la industria/rubro del usuario, reduciendo el rebote e incentivando la navegación interna hacia el blog.

## 2. Requisitos Exactos
1. **Ubicación en la Maquetación**:
   - La sección debe ir inmediatamente debajo del bloque de "Ciudades Hermanas" (`{CIUDADES_HERMANAS_HTML}`) y antes del pie de página (`{FOOTER_HTML}`) en `templates/template.html`.
2. **Carga y Filtrado por Rubro (Industria)**:
   - Se leerá la lista de blogs publicados desde `data/published_blogs.json`.
   - Para cada landing page, se buscará un artículo que coincida con el rubro (industria) de la página (ej. para la landing de Restaurantes, el artículo principal recomendado será `ia-para-restaurantes` u otro con categoría/título similar).
   - Se completará la recomendación con 2 artículos de interés general (ej. sobre precios, diferencias de bots, casos de éxito, etc.) para formar siempre un bloque de **3 tarjetas de recomendación**.
   - Si una industria no cuenta con un artículo específico, se seleccionarán 3 artículos generales/populares como comodines.
3. **Cálculo de Tiempo de Lectura Dinámico**:
   - En el script `build.py`, se calculará de forma dinámica el tiempo estimado de lectura de cada artículo analizando el archivo de contenido real (ej. leyendo `dist/blog/{slug}/index.html` o a partir de una estimación de longitud de palabras estándar) asumiendo una velocidad promedio de 200 palabras por minuto.
   - El resultado se mostrará en la tarjeta con el texto: `Lectura: X min`.
4. **Diseño Visual de las Tarjetas (Alineación y Animaciones)**:
   - Disposición en grilla de 3 columnas (`grid grid-cols-1 md:grid-cols-3 gap-8`).
   - Título de la sección premium y persuasivo: *"Aprende a Escalar y Automatizar tu Negocio con Inteligencia Artificial"*.
   - Tarjetas modernas con bordes redondeados (`border border-gray-border dark:border-zinc-800 rounded-3xl`).
   - Efecto hover interactivo: elevación sutil de la tarjeta (`transform: translateY(-4px)`) y zoom suave de la imagen de portada (`scale: 1.05` con transición suave).
5. **Botón de Enlace al Blog**:
   - Debajo de las 3 tarjetas, un botón minimalista y elegante centrado con el texto *"Ver todos los artículos"* que redirija a `/blog/`.

## 3. Casos de Borde (Edge Cases)
1. **Industrias sin artículo específico**: Si la industria de la landing page no tiene una correspondencia en `data/published_blogs.json`, el sistema debe elegir automáticamente los 3 artículos generales más recientes.
2. **Archivos HTML del blog inexistentes o corruptos**: Si al compilar las landings no se encuentra el archivo del blog en `dist/blog/{slug}/index.html` para calcular las palabras, se debe aplicar un fallback por defecto de `5 min` para evitar que el script falle.
3. **Menos de 3 artículos disponibles**: Si la caché de `published_blogs.json` tiene menos de 3 artículos, la grilla mostrará los que existan sin generar errores visuales ni romper el grid layout.

## 4. Definición de Hecho (Definition of Done)
- [ ] La sección de recomendación de blogs aparece correctamente en todas las landings generadas por `build.py`.
- [ ] En las landings de rubros específicos (ej. Restaurantes, Salones de Belleza), la primera tarjeta muestra el artículo específico de su industria.
- [ ] El tiempo de lectura estimado se calcula y se muestra de forma dinámica en cada una de las 3 tarjetas.
- [ ] El diseño CSS implementa los efectos de zoom en hover sobre las imágenes y la elevación de las tarjetas.
- [ ] El botón minimalista "Ver todos los artículos" está centrado y redirige correctamente a `/blog/`.
- [ ] El script `build.py` se ejecuta sin errores y genera las 436 landings actualizadas.
