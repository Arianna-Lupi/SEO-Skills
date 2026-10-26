---
name: sitemap-y-robots
description: Revisa y genera el robots.txt y el sitemap.xml de un sitio, y comprueba que no haya bloqueos accidentales, noindex ni canonicals que contradigan al sitemap. Usa esta skill cuando haya que mirar cómo Google descubre y rastrea un sitio, AUNQUE el usuario no diga "sitemap" ni "robots", p.ej. "Google no me encuentra las páginas nuevas", "creo que bloqueé mi web", "Search Console dice sitemap con errores", "no sé si mi robots.txt está bien", "mi sitio hecho en Next.js no tiene sitemap", "las IAs no me citan, ¿las estoy bloqueando?", "Descubierta, actualmente sin indexar". Sigue la Semana 3 y la Semana 12 del diplomado "De Cero a SEO" (rastreo, indexabilidad, "lo que no se rastrea, no existe") y entrega hallazgos por severidad, el archivo corregido o el ticket para el developer.
compatibility: Scripts en Python 3 solo con stdlib (revisar_robots_sitemap.py y generar_sitemap_robots.py), sin claves. Las lecturas en vivo van al propio sitio con User-Agent de navegador, ritmo lento y respetando robots.txt; si un WAF (Cloudflare) bloquea, cae a modo manual con technicalseo.com y la exportación del sitemap desde Search Console. GSC MCP opcional.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/sitemap-robots.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `sitemap-robots.json`.

# Sitemap y robots.txt (Diploma S3 y S12)

Actúa como Ingeniero SEO técnico en aprendoseo. Filosofía del diploma: *"Lo que no se rastrea, no existe"* y *"Menos es más si es lo correcto"*: en el sitemap solo va lo que quieres posicionar, y en el robots.txt solo se bloquea lo realmente privado. Metáfora de Juan Carlos Angulo: Googlebot es un **turista**; el robots.txt le dice por qué calles puede pasar y el sitemap es el **mapa oficial**.

> **Método del diploma:** lecciones, prompts y criterios de coaches en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lo que viene de claude-seo (límites del sitemap, lastmod, lista de bots de IA, casos límite) está separado y es opcional: [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md).

## Cuándo usar

- Google no indexa o descubre páginas nuevas, o GSC marca errores de lectura en el sitemap.
- Sospecha de bloqueo accidental (`Disallow: /`, recursos o autores bloqueados).
- Primer paso del **Bloque 1** de `auditoria-tecnica` (indexabilidad y rastreabilidad).
- Sitio nuevo, migración o rediseño: hay que crear o validar ambos archivos.
- El usuario pregunta si bloquea a las IAs (GPTBot, ClaudeBot, PerplexityBot...).

## Entradas

- **Dominio** (obligatorio). Qué **CMS** usa y si está detrás de **Cloudflare** (Juan siempre lo pregunta: define qué es realizable).
- Opcional: captura de GSC > Sitemaps y de "Indexación > Páginas", o el robots.txt pegado a mano.
- Para generar: lista de URLs (usa `inventario-de-urls`) y cuáles excluir.

## Pasos (método del diploma)

1. **Abre `dominio.com/robots.txt`** (S3, S12). Busca `Disallow: /` sobre lo que quieres posicionar. Un 302 en el rastreo suele venir de un bloqueo. Comprueba que no bloquee autores (`/author`), imágenes, CSS ni JS.
2. **Busca el sitemap** en `dominio.com/sitemap.xml` (S3, acción de Trello "Verificación de mapas") y en las líneas `Sitemap:` del robots.txt. En GSC > Sitemaps verifica que se **procesó recientemente y sin errores de lectura** (S12).
3. **Compara lo indexado con lo esperado** con `site:dominio.com` (S3). Si aparecen carpetas de administración o basura, anótalo.
4. **Revisa `noindex` y canonical** de una muestra de URLs del sitemap: un sitemap no debe listar URLs con `noindex`, redirigidas ni canonicalizadas a otra.
5. **Ejecuta el script** para automatizar los pasos 1 a 4 (abajo) y complétalo con GSC.
6. **Clasifica por severidad** y por plantilla, y redacta cada tarea con **verbo**, **explainer** (qué es / por qué importa / cómo se soluciona), **evidencia** real e **ICE**. Solo tareas realizables según el CMS (ver Reglas).
7. Si el arreglo es de código, entrega el **ticket para el developer** (S13 · "El Rol del SEO Técnico"): por qué afecta, qué cambiar y el archivo corregido.
8. **Cierra en dashboard** (`dashboard-seo`).

## Script determinista (ahorro de tokens)

```
# Revisión completa: robots.txt, bots de IA, sitemaps (índices y .gz) y muestra de 20 URLs
python3 skills/sitemap-y-robots/scripts/revisar_robots_sitemap.py https://ejemplo.com --site ejemplo.com
# Probar rutas contra el robots.txt (equivale a technicalseo.com/tools/robots-txt)
python3 skills/sitemap-y-robots/scripts/revisar_robots_sitemap.py https://ejemplo.com --probar /blog/ /author/ /wp-admin/ --muestra 40
# Generar sitemap.xml (+ robots.txt base) desde una lista de URLs
python3 skills/sitemap-y-robots/scripts/generar_sitemap_robots.py --base https://ejemplo.com --urls urls.txt --excluir excluir.txt --robots --ia permitir --out ./salida
```

Salida del primero: `{"ok","robots":{...,"ai_bots":{...}},"sitemap":{"files","total_urls","sample"},"issues":[{"severity","where","issue","fix"}]}`. Si no puede leer el sitio devuelve `{"ok":false,"blocked":...,"fallback":"modo manual..."}`: sigue con technicalseo.com y la exportación desde GSC. **No intentes evadir un WAF.** El generador **no inventa fechas**: sin CSV de fechas reales no escribe `lastmod`.

## Salida

- Tabla de hallazgos (severidad, dónde, qué pasa, cómo se arregla) lista para la pestaña **Auditoría** de la Plantilla Master.
- Archivos `sitemap.xml` / `robots.txt` corregidos cuando aplique, o ticket para el developer.
- Lista de URLs afectadas **en un Sheet**, no en el texto.
- `sitemap-robots.json` en `.seo-audit/<sitio>/data/`.

| Severidad | Ejemplo | Acción |
|---|---|---|
| Crítico | `Disallow: /` en User-agent * | Quitar la regla y reenviar el sitemap en GSC |
| Alto | Sitemap con URLs `noindex` o 404 | Quitarlas del sitemap |
| Medio | robots.txt sin línea `Sitemap:` | Agregarla |
| Bajo | `priority`/`changefreq` en el sitemap | Opcional: quitar, Google los ignora |

## Reglas

- **robots.txt es una guía, no una barrera**: los bots pueden ignorarla. Para ocultar algo de verdad usa `noindex` o contraseña (práctica de coaches, Juan).
- **Realizable según el CMS:** en WordPress el sitemap lo generan Rank Math o Yoast (no listas manuales); en **Shopify** el robots.txt sí es editable pero el sitemap se crea solo y no se edita; en sitios hechos con código (Next.js) el sitemap y el robots **los genera un developer**: si dan 404, faltan.
- **Cloudflare** suele inyectar reglas que bloquean crawlers de IA; se editan desde Cloudflare. Una mala configuración puede evitar que las IAs te citen.
- **"Descubierta, actualmente sin indexar" no significa que falte en el sitemap:** inspecciona la URL en GSC y mira "páginas de referencia".
- Probar el robots.txt en **technicalseo.com/tools/robots-txt**. El modo de IA de Octopus **inventa** el mapa: para generar un sitemap real usa su generador (`octopus.do/sitemap/generator`, hasta 500 URLs gratis) o el script.
- Divi y parámetros `?et_blog`: se resuelven con una regla en robots.txt.
- Sitemap y robots **no se contradicen**: lo que está en el sitemap no puede estar bloqueado.
- **Nunca inventes** el número de URLs indexadas ni fechas de modificación. Lo que falte, se pide.
- Complementos opcionales (después del método): límites de 50.000 URLs/50 MB, lastmod fiable, sitemaps de imágenes y bots de IA en [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md).

## Gotchas

- Un cambio en robots.txt puede tardar en reflejarse; revisa la caché del plugin o de Cloudflare y prueba en incógnito.
- Algunos sitios bloquean a Screaming Frog por carga al servidor; no es un error del sitio.
- `Allow: /` desde la raíz está bien. `Crawl-delay` frena rastreos rápidos, pero Google lo ignora.
- Si la verificación por DNS en GSC falla, usa la etiqueta HTML en el head.
