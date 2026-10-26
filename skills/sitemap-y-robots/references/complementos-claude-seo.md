# Complementos de claude-seo para sitemap y robots

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.**
> Fuente: `skills/seo-sitemap/SKILL.md`, `skills/seo-technical/SKILL.md`, agente `seo-sitemap` y `scripts/sitemap_discovery.py` del repo AgriciDaniel/claude-seo (licencia MIT). Adaptado al español y a la terminología del curso. Si algo contradice el diplomado, gana el diplomado.

## 1. Validación del sitemap

- XML válido. Un archivo admite **hasta 50.000 URLs y 50 MB sin comprimir** (lo que ocurra antes); por encima, **sitemap índice**.
- Todas las URLs deben responder **200**, ser **https**, **canónicas** y **sin noindex ni redirección**.
- **`<lastmod>`:** formato W3C (AAAA-MM-DD) y fecha del último cambio **significativo** del contenido (no del pie de página). Google solo lo considera si es fiable; valores idénticos en todas las URLs o más nuevos que el contenido real le restan valor.
- **`<priority>` y `<changefreq>`** los ignora Google: se pueden quitar (hallazgo informativo).
- El sitemap debe estar referenciado en robots.txt y enviado en GSC.
- Compara lo rastreado con lo listado: páginas indexables que faltan en el sitemap son un hallazgo.
- Divide por tipo de contenido (páginas, entradas, imágenes, videos) en sitios grandes; facilita ver en GSC qué sección falla.

| Hallazgo | Severidad sugerida |
|---|---|
| Más de 50.000 URLs o 50 MB en un archivo | Crítico |
| URLs que no son 200 en el sitemap | Alto |
| URLs con noindex en el sitemap | Alto |
| URLs redirigidas en el sitemap | Medio |
| lastmod idéntico en todas | Bajo |
| priority/changefreq presentes | Informativo |

## 2. Sitemaps de extensión (imágenes, video, noticias)

- **Imágenes:** solo `<image:image>` y `<image:loc>` siguen vigentes (hasta 1.000 imágenes por URL). Caption, title, geo_location y license se retiraron en 2022.
- **Video:** requiere `<video:thumbnail_loc>`, `<video:title>`, `<video:description>` y `<video:content_loc>` o `<video:player_loc>`.
- **Noticias:** máximo 1.000 `<news:news>` por archivo y solo artículos de los últimos 2 días.

Si el sitio no es de noticias ni video, ignora esta sección: "menos es más si es lo correcto".

## 3. Páginas generadas a escala (calidad antes que cantidad)

claude-seo pone barreras al crear sitemaps de muchas páginas parecidas: advertencia desde unas 30 páginas de ubicación y parada desde unas 50 sin justificación, y exigir contenido único (más del 60%). Es una regla de seguridad contra contenido delgado, alineada con "menos es más". Seguras a escala: integraciones con documentación real, plantillas descargables, glosarios con definiciones propias, fichas de producto con datos únicos. Riesgo: páginas por ciudad que solo cambian el nombre, "mejor X para Y" sin valor propio, "alternativa a Z" sin datos reales, contenido de IA sin revisión humana.

## 4. Rastreadores de IA y robots.txt

| Rastreador | Empresa | Uso |
|---|---|---|
| GPTBot | OpenAI | Entrenamiento |
| OAI-SearchBot | OpenAI | Búsqueda de ChatGPT |
| ChatGPT-User | OpenAI | Navegación a pedido del usuario |
| ClaudeBot | Anthropic | Entrenamiento |
| Claude-User | Anthropic | Navegación a pedido del usuario |
| PerplexityBot | Perplexity | Índice de búsqueda |
| Google-Extended | Google | Entrenamiento de Gemini (**no** afecta a Search ni a AI Overviews) |
| Applebot-Extended | Apple | Entrenamiento |
| Bytespider | ByteDance | Entrenamiento |
| CCBot | Common Crawl | Dataset abierto |

- Bloquear `Google-Extended` no toca la indexación de Google Search. Bloquear `GPTBot` frena el entrenamiento de OpenAI, pero no impide que ChatGPT navegue tu sitio con `ChatGPT-User`.
- Los fetchers disparados por el usuario (por ejemplo agentes de Google) pueden ignorar robots.txt por diseño: para controlarlos hace falta control de acceso en el servidor.
- Decide según tu estrategia de visibilidad en IA (skill `optimizacion-geo-aeo`): bloquear al entrenamiento no es lo mismo que bloquear a los buscadores de IA que te citan. Pregunta al cliente antes de bloquear.
- Esta lista cambia: confirma los nombres vigentes en la documentación de cada empresa antes de entregar un robots.txt.
- Ejemplo de bloqueo selectivo (solo entrenamiento): un grupo `User-agent: GPTBot` con `Disallow: /`, otro para `ClaudeBot`, `Google-Extended`, etc., y el grupo `User-agent: *` con `Allow: /`. El script `generar_sitemap_robots.py --ia bloquear-entrenamiento` lo escribe.

## 5. Descubrimiento de sitemaps (casos límite)

- Lee **todas** las líneas `Sitemap:` de robots.txt (puede haber varias) y prueba rutas comunes aunque una declarada falle.
- No declares "no hay sitemap" hasta haber probado ambas vías. Una línea `Sitemap:` en robots.txt no prueba que funcione: lee el archivo.
- Una declaración con `http://` en un sitio `https` es un hallazgo.

## 6. Límites de rastreo de Google

- Googlebot lee los primeros **2 MB de HTML**; el tope de un PDF es mayor. Contenido o JSON-LD pasado ese límite no se indexa.
- La velocidad de rastreo se ajusta sola (se frena con errores 5xx o respuestas lentas). Ya no existe el control manual de velocidad en Search Console.

## 7. Qué quedó fuera

- IndexNow (aviso inmediato a Bing/Yandex/Naver) y `llms.txt`: no los usa Google Search; no son parte del diplomado. Si el usuario los pide, usa los scripts `indexnow_submit.py` de claude-seo con permiso explícito, porque envían URLs a terceros.
