# Método del diploma: velocidad y rendimiento (Semanas 3 y 12)

> Fuente: resúmenes oficiales del diplomado "De Cero a SEO" (aprendoseo, Arianna Lupi). Material en `data/diplomado/docs/`.

## Qué enseña el curso

**Semana 12 · "Velocidad y rendimiento" (Bloque 2 de la auditoría técnica)**

1. Los **Core Web Vitals** son las métricas de experiencia: **LCP** (carga del elemento principal), **FID/INP** (respuesta e interacción; hoy se mide INP) y **CLS** (estabilidad visual, que los elementos no "salten").
2. **Categorizar por plantillas:** en vez de revisar 1.000 páginas, audita las plantillas principales (Home, Categoría/Blog, Producto/Artículo) para encontrar errores **sistémicos**.
3. Pasa las **3 plantillas principales por PageSpeed Insights** y anota los valores de Core Web Vitals.
4. **Imágenes, el factor de peso:** formato moderno (WebP), peso reducido (listar y comprimir las que superen **100 kb**), dimensiones acordes al diseño y atributo ALT. Detalle en la skill `optimizacion-de-imagenes`.
5. Tip: **"Optimiza el contenedor, no solo el contenido."** De nada sirve una imagen optimizada si la plantilla es lenta; hay que saber si el problema es un caso aislado o un error de diseño que afecta a todo el sitio.

**Semana 3 · "Cuáles son las herramientas del SEO Técnico"**: PageSpeed Insights y Lighthouse para medir la velocidad (WPO) e identificar imágenes pesadas y código innecesario. Consejo de Juan Carlos Angulo: empieza dominando `site:` y PageSpeed, que son gratuitas, antes de herramientas complejas.

**Acciones para tu Trello (S12):** pasar las 3 plantillas (Home, Categoría, Artículo) por PageSpeed Insights y anotar los CWV; inventariar imágenes de más de 100 kb y planificar su compresión. **S3:** pegar la URL en PageSpeed y anotar el puntaje actual como punto de partida técnico.

**Prompt oficial (S12 · video 3):** "Actúa como Especialista en Web Performance (WPO) en aprendoseo. Analiza los resultados de rendimiento de mi sitio [Insertar Datos de PageSpeed]. Identifica cuál de los Core Web Vitals está afectando más mi puntuación, sugiere técnicas de optimización de imágenes específicas y verifica si mi estructura de URLs canónicas es la correcta para evitar problemas de contenido duplicado."

## Práctica de coaches (Juan Angulo, SEO técnico)

- Herramientas que usa: PageSpeed Insights, Lighthouse en pestaña de incógnito cuando PageSpeed no abre, y Unlighthouse con `npx unlighthouse --site https://dominio.com`.
- Lazy loading se comprueba con clic derecho, inspeccionar y buscar `loading=lazy`.
- En WordPress: Autoptimize, WP Rocket; demasiados plugins activos frenan la carga.
- Si los cambios tardan en verse, revisa el plugin de caché ("borrar caché al publicar o actualizar"), prueba en incógnito y valora Cloudflare.
- En Shopify no se pueden subir WebP/AVIF: se comprimen las imágenes.
