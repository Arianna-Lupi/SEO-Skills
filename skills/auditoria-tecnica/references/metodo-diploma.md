# Método del diploma — Auditoría técnica SEO (Semana 12, Arianna Lupi)

> Fuente: corpus interno "De Cero a SEO" (chunks, doc_type resumenes-prompts/transcripciones), Semana 12. Material de aprendoseo.

La auditoría técnica del diploma se ejecuta sobre un **formato/plantilla de tareas** y se divide en **3 bloques** que se hacen en orden. El formato fue rediseñado para ser "más ágil y digerible": *"Menos es más si es lo correcto"*.

## El método paso a paso (como lo enseña el curso)

El orden de la auditoría que dicta el curso (S12 transcripción, repaso de cierre):
> "hablaremos de la indexabilidad. El rastreo, el archivo robots.txt, el mapa del sitio, la arquitectura y los breadcrumbs. Luego... la auditoría técnica, cómo terminarla, asegurarnos que el sitio tenga este certificado SSL, que no haya errores de indexación."

**Bloque 1 — Indexabilidad y rastreabilidad** (video 2)
1. Distinguir **rastreabilidad (crawling)** —que los robots recorran el sitio por sus enlaces— de **indexabilidad** —que esas páginas entren al índice de Google.
2. Simular el rastreo de Google con **Screaming Frog**; filtrar por **Response Codes** para detectar 4xx/5xx.
3. Revisar el **robots.txt** (`tuweb.com/robots.txt`): que no haya un `Disallow: /` bloqueando páginas que quieres posicionar. Un 302 en el rastreo suele venir de un bloqueo en robots.txt.
4. Verificar en **Google Search Console** qué páginas se indexan y que el **Sitemap** se haya procesado sin errores de lectura.

**Bloque 2 — Velocidad y rendimiento (Core Web Vitals)** (video 3)
1. **Categorizar las páginas por plantillas** primero: en vez de revisar 1.000 páginas, identifica los diseños que se repiten (Home, Categoría/Blog, Producto/Artículo) y audita las plantillas para hallar errores **sistémicos**.
2. Pasar las 3 plantillas principales por **PageSpeed Insights** y anotar los Core Web Vitals (LCP, FID/INP, CLS).
3. **Optimizar imágenes** (el "fruto bajo" más rápido): formato moderno (**WebP**), peso reducido, dimensiones acordes al diseño y **atributo ALT** en cada imagen.
4. Introducir **canonicalización**: que las páginas clave sean **self-canonical** y no apunten a URLs erróneas.

**Bloque 3 — Seguridad y canonicalización** (video 4)
1. **Canonicalización profunda:** detectar duplicados (plugin de Ahrefs o Screaming Frog); definir la **URL maestra** que debe indexarse y hacer que las copias apunten a ella (`rel="canonical"`) para no diluir autoridad.
2. **Seguridad (HTTPS/SSL):** todo el sitio bajo HTTPS; que entrar por `http://` redirija a `https://`; sin **contenido mixto**.
3. Cerrar el documento marcando Seguridad y Canonicalización como "Finalizada".

## Plantillas, criterios y umbrales exactos

| Chequeo | Criterio / umbral del diploma | Herramienta |
|---------|-------------------------------|-------------|
| Códigos de respuesta | Buscar 200 OK; detectar 301/302, ausencia de 404 | Screaming Frog (Response Codes) |
| robots.txt | Sin `Disallow: /` sobre páginas a posicionar | Navegador (`/robots.txt`) |
| Sitemap | Procesado recientemente, sin errores de lectura | Google Search Console |
| Core Web Vitals | LCP (carga), FID/INP (interacción), CLS (estabilidad visual) por plantilla | PageSpeed Insights |
| Imágenes pesadas | Listar y comprimir imágenes que **superen los 100 kb**; usar WebP; ALT presente | Screaming Frog |
| Canonical | Páginas clave **self-canonical**; duplicados apuntando a la original | Screaming Frog / plugin Ahrefs (columna "Canonical") |
| Seguridad | HTTPS en todo el sitio; redirección http→https; sin contenido mixto; certificado SSL válido | Navegador / auditoría |

**Principio operativo:** auditar **por plantillas**, no página por página — "Optimiza el contenedor, no solo el contenido" (saber si un problema de velocidad es aislado o un error de diseño que afecta a todo el sitio).

## Prompts originales que da el curso (verbatim)

**Auditor de Infraestructura SEO (Semana 12, video 1):**
> "Actúa como Ingeniero SEO Técnico en aprendoseo. Ayúdame a revisar los cimientos de mi proyecto en aprendoseo. Analiza mi archivo Robots.txt y mi Sitemap [Insertar enlaces si existen] para asegurar que no estoy bloqueando por error secciones importantes y sugiere 3 acciones prioritarias para mejorar la velocidad de carga y la indexabilidad inmediata."

**Auditor de Performance y UX (Semana 12, video 3):**
> "Actúa como Especialista en Web Performance (WPO) en aprendoseo. Analiza los resultados de rendimiento de mi sitio en aprendoseo [Insertar Datos de PageSpeed]. Identifica cuál de los Core Web Vitals está afectando más mi puntuación, sugiere técnicas de optimización de imágenes específicas y verifica si mi estructura de URLs canónicas es la correcta para evitar problemas de contenido duplicado."

**Auditor de Seguridad y Duplicidad (Semana 12, video 4):**
> "Actúa como Consultor SEO Técnico Senior en aprendoseo. Revisa la configuración de seguridad de mi sitio en aprendoseo [Insertar URL] para detectar posibles problemas de contenido mixto. Además, analiza mis URLs para identificar contenido duplicado y sugiéreme cómo implementar correctamente las etiquetas canonical para consolidar la autoridad en las páginas que realmente quiero posicionar."

## Términos del diploma (definiciones)

- **Rastreabilidad (crawling):** capacidad de los robots de Google de recorrer el sitio a través de los enlaces.
- **Indexabilidad:** posibilidad de que las páginas rastreadas se incluyan en el índice de Google.
- **Auditoría por plantillas:** auditar los diseños de página que se repiten (Home, Blog, Producto) para detectar errores sistémicos en vez de revisar todas las URLs.
- **Core Web Vitals:** LCP (Largest Contentful Paint, carga del elemento principal), FID/INP (capacidad de respuesta e interacción), CLS (Cumulative Layout Shift, estabilidad visual).
- **Canonicalización / `rel="canonical"`:** indicar a Google la "versión maestra" de una página para evitar contenido duplicado. **Self-canonical** = la página apunta a sí misma como original.
- **Contenido mixto:** recursos cargados por `http` dentro de una página `https`; penalizado.
- **Breadcrumbs (migas de pan):** parte de la arquitectura/indexabilidad revisada en el bloque 1.

## Ejemplos del curso

- **"Lo que no se rastrea, no existe" (S12 chunk 2):** antes de preocuparse por keywords hay que garantizar el camino de Google despejado; un simple error en robots.txt puede dejar fuera tus páginas más importantes.
- **Categorización por plantillas (S12 transcripción):** "este diseño de página... es una imagen, texto, autor y todo el texto de blog" — se identifica el patrón y se audita una vez por plantilla.
- **Self vs non-canonical (S12 transcripción):** "vamos a ver que es self-canonical... no debería ser así, sino que debería ser non-canonical. Y la canonical es esta, la página original."
- **"Menos es más si es lo correcto" (S12 chunk 6):** una auditoría de 10 puntos críticos accionables hoy vale más que una de 100 páginas que nadie entiende.
