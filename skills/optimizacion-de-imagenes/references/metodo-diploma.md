# Método del diploma: imágenes, ALT y peso (Semanas 1, 10, 11, 12 y 14)

> Fuente: resúmenes oficiales del diplomado "De Cero a SEO" (aprendoseo, Arianna Lupi), `data/diplomado/docs/`. No hay una lección solo de imágenes: el criterio aparece en la auditoría técnica y en las lecciones de contenido y ecommerce.

## Qué enseña el curso

**Semana 12 · "Velocidad y rendimiento" (Bloque 2 de la auditoría técnica), la lección central**
- "Optimización de imágenes (el factor de peso)": uno de los puntos más críticos de la auditoría técnica.
  - **Peso y formato:** formatos modernos como **WebP** para reducir tamaño sin perder calidad.
  - **Atributos ALT:** cada imagen con su descripción, para accesibilidad y SEO de imágenes.
  - **Dimensiones:** que las imágenes no sean más grandes de lo que el diseño requiere.
- **Acción de Trello:** "Inventario de Imágenes Pesadas: usa Screaming Frog para listar todas las imágenes que superen los **100 kb** y planifica su compresión."
- Tip: **"Optimiza el contenedor, no solo el contenido."** De nada sirve una imagen optimizada si la plantilla es lenta; hay que ver si el problema es aislado o un error de diseño que afecta a todo el sitio.
- Prompt oficial (Auditor de Performance y UX): "...sugiere técnicas de optimización de imágenes específicas y verifica si mi estructura de URLs canónicas es la correcta..."

**Semana 12 · Core Web Vitals:** LCP (carga del elemento principal, muchas veces una imagen), CLS (estabilidad visual: que los elementos no "salten" mientras carga).

**Semana 1 · "Elementos de un Sitio Web":** Check de imágenes: todas las del contenido principal con tamaño ligero y texto alternativo.

**Semana 10 · brief/optimización de contenido existente para blog:** calidad visual, verificar que las imágenes tengan texto alternativo (Alt Text) para accesibilidad y SEO de imágenes.

**Semana 11 · Redacción SEO:** al menos una imagen con **nombre de archivo amistoso** y su ALT. Checklist: imagen lista con nombre descriptivo (ejemplo del curso: `guia-redaccion-seo.jpg`) y texto alternativo preparado.

**Semana 14 · SEO de ecommerce:** las fotos de producto con texto alternativo que describa qué es el artículo.

## Práctica de coaches (afina criterios, no sustituye el curso)

Fuentes: `data/voice-profile.md` (Juan Angulo), `data/coaches/diana.md`.

- **Prioridad al auditar:** botones rotos, H1 e imágenes pesadas, alta; falta de alt, baja.
- **Squoosh** es la herramienta que recomienda Juan para comprimir imágenes.
- **Shopify:** no admite subir WebP o AVIF; se comprimen las imágenes.
- **Lazy loading:** se verifica con clic derecho, inspeccionar, buscar `loading=lazy`.
- **WordPress:** WP Rocket y Autoptimize ayudan con la carga.
- **Tablas de especificaciones:** que se rendericen en HTML y no como imagen (Diana).
- **Un solo enlace por tarjeta** (imagen y nombre juntos) en listados: evita enlaces duplicados.
- **Auditorías para el cliente:** cada issue con qué es, por qué importa y cómo se soluciona; evidencia ("Evidencias del error") con antes y después; lista de URLs en un Sheet.

## Buenas prácticas de ALT que se derivan del curso

1. Descriptivo y breve: qué se ve y, si encaja, el contexto de la página. Una frase natural.
2. Sin repetir la keyword en todas las imágenes ni listar palabras clave.
3. Imágenes que solo decoran: `alt=""`.
4. Fichas de producto: nombre del producto y rasgo diferenciador (color, modelo).
5. Nombre de archivo en minúsculas, con guiones, descriptivo.
