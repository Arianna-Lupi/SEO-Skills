---
name: schema-jsonld
description: Usa esta skill cuando haya que generar datos estructurados Schema.org en JSON-LD válidos para una página, según el SEO técnico del diploma "De Cero a SEO" (aprendoseo). Aplícala siempre que publiques o reoptimices una página y quieras habilitar rich results (estrellas, FAQ, breadcrumbs, sitelinks) y reforzar entidades/autoría para la búsqueda con IA — aunque el usuario no diga "schema" ni "JSON-LD", p.ej. "quiero que me salgan las estrellas en Google", "habilita el desplegable de FAQ en la SERP", "datos estructurados para este artículo", "marca esta ficha de producto". Entrega el bloque `<script>` listo para pegar y validado. No marques contenido que no exista en la página: Google penaliza.
compatibility: Script opcional requiere Python 3 (uv, solo stdlib). Validación con Rich Results Test / validador schema.org (gratis). SerpApi MCP (GRATIS) o Ahrefs (pago) opcionales para ver qué rich results valen la pena.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

# Datos Estructurados / Schema.org en JSON-LD (SEO técnico)

Actúa como especialista en SEO técnico en aprendoseo. El schema no posiciona por sí solo, pero **ayuda a Google a entender la página** (apoya el flujo rastreo → indexación → rich results) y refuerza las **entidades y la autoría** que las IAs usan para citarte. Marco del diploma: *"Lo que no se rastrea, no existe"* — y lo que el buscador no entiende, no luce en la SERP.

## Cuándo usar

- Publicas una **página nueva** o reoptimizas una existente y quieres habilitar **rich results**.
- Tienes FAQs visibles, un producto con reseñas, un paso a paso (HowTo), migas de pan o una ficha de negocio.
- Quieres reforzar **autoría/Organization/WebSite** para E-E-A-T y GEO (complementa la skill `optimizacion-geo-aeo`).
- Estás cerrando la pestaña **Producción** o **Auditoría** de la Plantilla Master.

## Entradas (qué te doy)

- **URL o tipo de página** (home, artículo/blog, producto, FAQ, tutorial, ficha local…).
- **Contenido real visible** en la página (título, autor, fecha, precio, reseñas, preguntas, pasos).
- Marca / **Organization** (nombre, logo, redes) y datos del negocio si es local.
- Opcional: qué rich result te interesa habilitar.

## Datos (MCP opcional)

Esta skill **funciona sin ningún MCP**: el JSON-LD se genera y se valida con herramientas gratuitas de Google/schema.org.

1. **Sin MCP (manual — siempre válido):** identifica el tipo de página, escribe el JSON-LD y **valídalo** en el **Rich Results Test** de Google y en el **validador de schema.org**. Verifica en GSC el informe de "Mejoras" tras indexar.
2. **SerpApi MCP (GRATIS — principal):** `mcp__serpapi__search` con tu keyword → observa **qué rich results muestran los que ya rankean** (estrellas, FAQ desplegable, sitelinks, breadcrumbs). Así sabes qué schema vale la pena implementar para esa SERP.
3. **Ahrefs MCP (PAGO):** `mcp__claude_ai_Ahrefs__serp-overview` (features de la SERP), `...site-audit-issues` (detecta errores de datos estructurados a escala). Ahrefs es de pago.

Config de MCP: ver `../../MCP-SETUP.md`.

## Proceso

1. **Identifica el tipo de página → tipo de schema correcto:**
   - Home / sitio → `Organization` + `WebSite` (con `potentialAction` = `SearchAction` para la sitelinks searchbox).
   - Artículo / blog → `Article` o `BlogPosting` (con `author`, `datePublished`, `publisher`).
   - Producto → `Product` + `Offer` + `AggregateRating` (solo si las reseñas son reales y visibles).
   - Preguntas frecuentes → `FAQPage` (**solo si las FAQ están visibles en la página**).
   - Tutorial paso a paso → `HowTo`.
   - Navegación → `BreadcrumbList`.
   - Negocio físico → `LocalBusiness` (NAP: nombre, dirección, teléfono, horario).
2. **Genera el JSON-LD válido** con las propiedades **requeridas + recomendadas** del tipo. Usa `@context: "https://schema.org"`, `@type` correcto y URLs absolutas.
3. **Conecta entidades:** enlaza `author`/`publisher` a la `Organization` con `@id` para reforzar el grafo de entidades (clave para GEO/E-E-A-T).
4. **Valida** en **Rich Results Test** + validador de schema.org. Cero errores; resuelve los *warnings* que apliquen.
5. **Evita marcado inexistente:** todo lo que marques debe **existir y ser visible** en la página. FAQPage sin FAQs visibles, o ratings inventados, = **penalización manual**. No lo hagas.
6. **Registra** el bloque y el resultado de validación en la Plantilla Master; despliegue → Trello.

## Script determinista (ahorro de tokens)

Si Python 3 está disponible, **ejecuta el script** para construir y validar el JSON-LD en vez de escribirlo a mano: es determinista, ahorra tokens y evita marcado inventado. Usa su JSON (`jsonld`) como salida y `missing_required`/`warnings` como checklist.

Ejecuta (cero instalación, resuelve deps solo):

```bash
uv run skills/schema-jsonld/scripts/schema_gen.py \
  --type Article \
  --field headline="Título" \
  --field author='{"@type":"Person","name":"Arianna"}'
# o, si no usas uv: python3 skills/schema-jsonld/scripts/schema_gen.py --type Article --field headline="Título"
# o con un objeto completo:
uv run skills/schema-jsonld/scripts/schema_gen.py --type Product --json '{"name":"X","offers":{...}}'
```

Corre con `--help` para ver opciones.

Tipos soportados: `Article, BlogPosting, Product, FAQPage, HowTo, BreadcrumbList, LocalBusiness, Organization, WebSite`. Devuelve `{"ok":true,"type","jsonld":{...},"missing_required":[...],"warnings":[...]}`. **No marques contenido inexistente:** `FAQPage`/`HowTo` solo si las preguntas o pasos son visibles en la página (el script ya lo advierte). Solo stdlib. Si Python no está disponible, genera el bloque en **modo manual**.

## Salida

- **Bloque `<script type="application/ld+json">` listo para pegar** en el `<head>` (o antes de `</body>`).
- **Nota de validación:** "Validado en Rich Results Test, 0 errores".
- **Qué rich result habilita** (ej. "habilita FAQ desplegable en la SERP").
- Fila en la pestaña **Producción / Auditoría** de la Plantilla Master.

## Ejemplo

**Entrada:** artículo de blog con autor y fecha; SerpApi muestra que el top 3 luce breadcrumbs.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Qué es el linkbuilding y cómo aplicarlo en 2026",
  "datePublished": "2026-06-01",
  "dateModified": "2026-06-01",
  "author": {
    "@type": "Person",
    "name": "Arianna Lupi",
    "url": "https://aprendoseo.com/autora/arianna-lupi"
  },
  "publisher": {
    "@type": "Organization",
    "name": "aprendoseo",
    "logo": {
      "@type": "ImageObject",
      "url": "https://aprendoseo.com/logo.png"
    }
  },
  "mainEntityOfPage": "https://aprendoseo.com/blog/que-es-linkbuilding"
}
</script>
```

**Nota:** validado en Rich Results Test, 0 errores. Habilita marcado de artículo + autoría (refuerza E-E-A-T). Para breadcrumbs añadir un bloque `BreadcrumbList` aparte.

## Gotchas

- **NO marques contenido que no es visible en la página** (FAQPage solo si las FAQ se ven, ratings solo si las reseñas son reales y visibles) — Google penaliza con acción manual de spam.
- **Valida el JSON-LD (Rich Results Test + validador schema.org) antes de publicar**, no después: 0 errores y resuelve los warnings que apliquen.
- **Un tipo por intención de página** (Article / Product / FAQPage / HowTo…), no mezcles `@type` que se contradigan; conecta entidades con `@id` para un grafo coherente.
- Incluye las propiedades **requeridas**, no solo las opcionales (ej. `Article` sin `author`/`headline` no genera rich result).
- El schema **habilita rich results y entendimiento de entidades, no posiciona** — no es factor de ranking directo.
- **Revisa el informe de Mejoras en GSC tras desplegar**, no asumas que quedó bien: un error rompe el rich result en silencio.
