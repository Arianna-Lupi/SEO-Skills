---
name: optimizacion-de-imagenes
description: "Audita y optimiza las imágenes de un sitio para SEO y velocidad: peso (más de 100 kb), formato moderno (WebP), dimensiones, texto ALT, nombres de archivo y lazy loading. Usa esta skill cuando las imágenes puedan estar frenando o desposicionando una página, AUNQUE el usuario no diga \"imágenes\", p.ej. \"mi página carga lenta y tiene muchas fotos\", \"PageSpeed me dice que sirva formatos modernos\", \"el LCP es la foto principal\", \"qué alt le pongo a estas fotos\", \"las fotos de mi tienda pesan mucho\", \"la página salta mientras carga\". Sigue el Bloque 2 de la auditoría técnica (Semana 12 · Velocidad y rendimiento) del diplomado \"De Cero a SEO\": audita por plantillas, prioriza lo realizable según el CMS y entrega tareas con verbo, explainer y evidencia."
compatibility: Script en Python 3 solo con stdlib (auditar_imagenes.py); lee las páginas del propio sitio con User-Agent de navegador, ritmo lento y respetando robots.txt. Si un WAF bloquea, cae a modo manual con Screaming Frog (pestaña Images) o PageSpeed Insights. La conversión de archivos usa herramientas del usuario (Squoosh, cwebp), nunca se envían imágenes a terceros sin permiso.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/imagenes.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `imagenes.json`.

# Optimización de imágenes (Diploma S12, Bloque 2)

Actúa como especialista en rendimiento web en aprendoseo. Filosofía del diploma: **"Optimiza el contenedor, no solo el contenido"** (S12 · Velocidad y rendimiento): una imagen perfecta no sirve si la plantilla la carga mal, y un problema repetido en la plantilla de artículo se arregla una vez para todas las instancias. Las imágenes son el "fruto bajo" más rápido de la velocidad y la causa más frecuente de un LCP malo.

> **Método del diploma:** lecciones, acciones de Trello y criterios de coaches en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lo que viene de claude-seo (umbrales por tipo de imagen, AVIF, srcset, fetchpriority, CLS) es opcional y está aparte: [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md).

## Cuándo usar

- Bloque 2 de `auditoria-tecnica`, o después de `analisis-rendimiento` cuando señale imágenes pesadas.
- PageSpeed pide "formatos modernos", "dimensiona correctamente las imágenes" o "evita cambios de diseño".
- El LCP es una imagen. O el CLS salta por fotos sin espacio.
- Hay que escribir o revisar **ALT** y nombres de archivo (artículos, fichas de producto).

## Entradas

- **Una URL por plantilla** (Home, categoría, artículo, producto). No todas las páginas.
- **CMS** del sitio: define qué se puede hacer (Shopify no admite subir WebP/AVIF; WordPress sí con plugin o a mano).
- Opcional: export de Screaming Frog (pestaña Images, filtro de más de 100 kb y sin alt).

## Pasos (método del diploma)

1. **Elige las plantillas** y una URL representativa de cada una.
2. **Inventario de imágenes pesadas** (S12, acción de Trello): lista las que superan **100 kb**. Con Screaming Frog (Images) o con el script.
3. **Revisa formato:** WebP en lugar de JPG/PNG cuando el CMS lo permite; si no, comprimir (Squoosh).
4. **Revisa dimensiones:** que la imagen no sea más grande de lo que el diseño muestra.
5. **Revisa ALT** en cada imagen que aporte contenido: descripción breve y útil (accesibilidad + SEO de imágenes). Nombre de archivo descriptivo (`guia-redaccion-seo.jpg`, no `IMG_1234.jpg`).
6. **Revisa estabilidad y carga:** `width`/`height` declarados (CLS), la imagen principal **sin** lazy loading, el resto con `loading="lazy"` (se comprueba con clic derecho, inspeccionar, buscar `loading=lazy`).
7. **Prioriza por plantilla** e impacto (cuántas páginas comparten el problema), no por imagen.
8. **Redacta cada tarea** empezando con verbo ("Comprimir...", "Convertir...", "Agregar alt..."), solo si es realizable según el CMS, con **explainer** (qué es / por qué importa / cómo se soluciona), **evidencia** real (captura de PageSpeed o fila del export), **ICE**, y la **lista de URLs/archivos en un Sheet**.
9. **Cierra en dashboard** (`dashboard-seo`).

## Script determinista (ahorro de tokens)

```
python3 skills/optimizacion-de-imagenes/scripts/auditar_imagenes.py https://ejemplo.com/ https://ejemplo.com/blog/articulo/ --site ejemplo.com
python3 skills/optimizacion-de-imagenes/scripts/auditar_imagenes.py --file plantillas.txt --max-imagenes 40
```

Salida: `{"ok","pages":[{"page","images":[{"src","kb","format","alt","width","height","loading","problems":[...]}],"findings":[{"severity","issue","fix"}]}]}`. El peso sale de los encabezados HTTP reales (nunca estimado). Si no puede leer el sitio devuelve `ok:false` con `fallback`: usa Screaming Frog (Images) o PageSpeed. **No intentes evadir un WAF.** Máximo 15 páginas por corrida.

## Salida

- Tabla por plantilla: imagen o grupo, peso, formato, problema, tarea.
- Tareas con verbo + explainer + evidencia + ICE; lista de archivos en un Sheet.
- `imagenes.json` en `.seo-audit/<sitio>/data/`.

| Plantilla | Problema | Severidad | Tarea |
|---|---|---|---|
| Artículo | Hero de 480 kb en JPG con LCP alto | Alto | Convertir el hero a WebP y reducir a las dimensiones del diseño |
| Producto | 14 fotos sin alt | Bajo | Agregar alt con nombre del producto y variante |
| Home | Slider sin width/height (CLS) | Medio | Declarar dimensiones en el contenedor |

## Reglas

- **Umbral del diploma: 100 kb.** Las de más de 100 kb se listan y se comprimen. Los umbrales por tipo de imagen del complemento son opcionales.
- **Prioridad (práctica de coaches):** imágenes pesadas, alta; falta de alt, baja. Primero lo que mueve el LCP.
- **Realizable según el CMS:** Shopify no admite subir WebP o AVIF, se comprimen los archivos; en WordPress se usa Squoosh, un plugin de optimización o la conversión de WP Rocket. No recomiendes lo que el CMS no permite.
- **El ALT describe, no rellena:** nada de listas de keywords. Imagen decorativa, `alt=""`. Tablas de especificaciones deben estar en HTML y no como imagen (práctica de coaches, Diana).
- **No toques la imagen principal con lazy loading.** El lazy es para lo que queda bajo el pliegue.
- **Nunca inventes pesos ni ahorros.** Sin medición real: `pendiente de dato`.
- Complementos opcionales (AVIF, srcset, fetchpriority, `decoding`, metadatos): solo después del método.

## Gotchas

- Un servidor que no responde HEAD devuelve peso vacío: el script reintenta con un rango de 1 byte; si aun así no hay dato, queda `kb: null`.
- Las imágenes cargadas por JavaScript (sliders, CSR) pueden no aparecer en el HTML crudo: revisa también en Screaming Frog con renderizado JS o en PageSpeed.
- Una CDN o Shopify puede servir WebP aunque el archivo original sea JPG: el script mide lo que el servidor entrega con la URL, no el archivo subido.
- Si cambias el nombre del archivo, actualiza las referencias y redirige la URL antigua si estaba indexada en imágenes.
