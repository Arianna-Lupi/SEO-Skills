---
name: seo-ecommerce
description: "Usa esta skill cuando el sitio sea una tienda online o tenga productos y colecciones, aunque el usuario no diga \"SEO de ecommerce\", p.ej. \"optimiza mi tienda Shopify\", \"cómo estructuro las colecciones\", \"mis productos no salen en Google\", \"qué título y descripción pongo a este producto\", \"tengo variantes y filtros y no sé qué indexar\", \"las paginaciones me duplican contenido\", \"marca esta ficha de producto con estrellas y precio\". Sigue el método de \"De Cero a SEO\" (aprendoseo, Semana 14, \"¿Qué es el SEO de ecommerce?\"): keywords transaccionales, categorías o colecciones como páginas críticas, fichas de producto con título, descripción persuasiva, FAQ, prueba social y alt text, más la práctica de Shopify de los coaches. Entrega estructura de colecciones, auditoría de fichas y schema Product listo."
compatibility: Script opcional requiere Python 3 solo con stdlib (auditar_producto.py, rastreo en vivo con User-Agent de navegador). Funciona 100% manual sin él. Shopify MCP y Merchant Center son opcionales.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/ecommerce.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `ecommerce.json`.

# SEO de ecommerce (S14)

Actúa como **Especialista en Conversión SEO en aprendoseo**. A diferencia de un blog, una tienda tiene un objetivo único: **vender**. Eso cambia las keywords (transaccionales: "comprar zapatos de cuero", "precio de laptops") y la estructura. Frase del curso: *"el norte es siempre la palabra clave"*; optimizar una tienda es facilitar el camino de la búsqueda al carrito.

> **Método completo del diploma:** [`references/metodo-diploma.md`](references/metodo-diploma.md). Detalles de colecciones, variantes, paginación y filtros en [`references/estructura-tienda.md`](references/estructura-tienda.md).

## Cuándo usar

- Tienda en Shopify, WooCommerce, Tiendanube u otra, nueva o existente.
- Hay que decidir la jerarquía de colecciones, qué se indexa y cómo se escriben las fichas.
- El usuario quiere estrellas, precio y disponibilidad en Google (schema de producto).

Antes: `investigacion-de-keywords` (keywords transaccionales) y `mapa-de-palabras-clave`. Durante: `arquitectura-y-enlazado-interno`, `brief-de-contenido` (variante E-commerce), `schema-jsonld`. Después: `plan-seo` para tareas y fechas.

## Entradas

- URL de la tienda, plataforma (Shopify u otra) y catálogo aproximado (cuántos productos y colecciones).
- Los 5 productos más vendidos y las colecciones principales.
- Si es Shopify con MCP conectado, lee colecciones y productos reales con `search_collections` y `search_products` en vez de pedirlos a mano.
- Datos reales de precio, stock, reseñas. No se inventan.

## Pasos

1. **Define el objetivo y las keywords transaccionales.** Un producto, una intención de compra. "El norte es la palabra clave": usa los términos que el cliente busca. Usa `investigacion-de-keywords`; sin volumen real, `pendiente de dato`.
2. **Mapa de las tres páginas críticas.**
   - **Colecciones o categorías**: las más importantes, para términos genéricos ("ropa de invierno").
   - **Productos**: ultra detalladas, resaltan características, beneficios y objeciones.
   - **Soporte**: FAQ, envíos, devoluciones, que dan confianza para comprar.
3. **Estructura de colecciones.** Jerarquía padre e hijas (una categoría padre con al menos dos hijas), cada colección apunta a **una** keyword útil, sin multiplicar colecciones al mismo nivel (diluyen). Divide lo amplio ("disfraces para niños" en edad, tema, personaje). Nombres estables, no menús semanales. Detalle en `references/estructura-tienda.md`.
4. **Ficha de producto, checklist del curso.**
   - Título optimizado con la keyword principal.
   - Descripción persuasiva, **no la del fabricante**, con características, beneficios y objeciones.
   - Sección de FAQ (pagos, envíos, tallas, garantía).
   - Prueba social: reseñas y valoraciones.
   - Imágenes con **texto alternativo** que describa el artículo.
   - Meta descripción transaccional: atributos, precio o envío.
5. **Canónicas, variantes, paginación y filtros.** Aplica los criterios de `references/estructura-tienda.md` (práctica de coaches con Shopify). Cualquier cambio de código del tema lo implementa o lo valida quien tenga acceso.
6. **Schema de producto.** Genera `Product` con `schema-jsonld`: `name`, `image`, `offers` (precio numérico, moneda ISO, disponibilidad), y si existen en la página: `sku`, `brand`, `aggregateRating`. Marca solo lo visible. Las migas de pan (`BreadcrumbList`) van en las páginas internas, no en la Home.
7. **Enlazado interno.** Migas de pan, productos relacionados, enlace de la ficha a su colección y de la colección a sus hijas. Cada página a máximo 3 clics de la Home.
8. **Auditoría de las 5 fichas más vendidas.** Usa `scripts/auditar_producto.py` (o a mano) y pasa los hallazgos a `plan-seo`.
9. **Cierre.** Persiste los hallazgos y entrega el dashboard.

## Script opcional

`scripts/auditar_producto.py <url-producto>` hace un solo fetch (User-Agent de navegador, respeta robots.txt, detecta WAF) y revisa: título y meta (longitud), H1 único, canónica, JSON-LD `Product` (campos obligatorios y recomendados, precio numérico, disponibilidad como URL), migas de pan, imágenes sin `alt` y señal de FAQ. Salida JSON; con `--sitio` guarda `.seo-audit/<sitio>/data/ecommerce.json`.

```bash
python3 scripts/auditar_producto.py --help
python3 scripts/auditar_producto.py https://tienda.com/products/zapato --sitio tienda.com
```

## Salida

```
SEO ECOMMERCE: [tienda] · Plataforma: ...
1. ESTRUCTURA: árbol de colecciones (padre > hijas) con keyword por colección
2. FICHAS: tabla producto | título | meta | H1 | FAQ | reseñas | alt | schema | hallazgos
3. TÉCNICO: canónicas, variantes, paginación, filtros (decisión y motivo)
4. SCHEMA: bloque Product validado por ficha tipo
5. TAREAS con verbo y prioridad (para plan-seo)
```

## Reglas

- Un producto o una colección, una keyword principal. No canibalices (`deteccion-de-canibalizacion`).
- No copies descripciones del fabricante. La IA puede dar el borrador masivo, pero revisa que sea útil y único.
- Schema solo con datos visibles en la página. No marques reseñas que no existan.
- No inventes precios, stock, reseñas ni ventas.
- Lo que el CMS no permita se difiere al developer.

## Complementos opcionales (claude-seo)

Después del método del diploma, [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md) añade una rúbrica de puntaje de ficha, reglas de validación de `Product`, brechas orgánico vs Google Shopping y una nota sobre protocolos de compra con IA. Algunos usos requieren servicios de pago.

## Gotchas

- Una colección amplia sin keyword clara no posiciona. "La colección no es una página SEO" solo si no se trabaja con su keyword.
- En Shopify el robots.txt es editable; el sitemap se genera solo y no se edita. No admite WebP/AVIF subidos: comprime las imágenes antes.
- La colección "all" no se puede borrar; solo ocultar quitando enlaces.
- Muchos filtros indexables generan duplicados: decide qué se indexa antes de abrir el rastreo.
