# Complementos de claude-seo para la auditoría técnica

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.**
> Fuente: `skills/seo-technical/SKILL.md`, `skills/seo-drift/references/comparison-rules.md` y scripts `drift_*.py` del repo AgriciDaniel/claude-seo (licencia MIT). Todo está adaptado al español y a la terminología del curso. Si algo de aquí contradice el diplomado, **gana el diplomado** (ver `metodo-diploma.md`). Usa esto después de completar los 3 bloques, nunca en su lugar.

## 1. Umbrales vigentes de Core Web Vitals

Se evalúan con datos de **campo** (percentil 75 de usuarios reales, CrUX o Search Console). Los datos de Lighthouse son de laboratorio y solo sirven para diagnosticar.

| Métrica | Bueno | Necesita mejora | Malo |
|---|---|---|---|
| LCP | hasta 2,5 s | 2,5 a 4 s | más de 4 s |
| INP | hasta 200 ms | 200 a 500 ms | más de 500 ms |
| CLS | hasta 0,1 | 0,1 a 0,25 | más de 0,25 |

- **INP** reemplazó a FID en marzo de 2024. No cites FID en informes nuevos (el diplomado lo nombra como "FID/INP", mide INP).
- Los rangos "necesita mejora" y "malo" son los publicados por Google en web.dev; confírmalos ahí si el informe es contractual.

## 2. Cabeceras de seguridad

El diplomado exige HTTPS, redirección http a https y ausencia de contenido mixto. Estas cabeceras van un paso más allá y son de prioridad **baja o media**: solo HTTPS es una señal de ranking confirmada, y es ligera. No les des más peso que a un canonical roto.

| Cabecera | Para qué sirve | Severidad sugerida si falta |
|---|---|---|
| Strict-Transport-Security (HSTS) | Obliga al navegador a usar https | Media |
| Content-Security-Policy | Limita qué recursos puede cargar la página | Baja |
| X-Frame-Options | Evita que embeban tu sitio en un iframe ajeno | Baja |
| X-Content-Type-Options | Evita que el navegador "adivine" tipos de archivo | Baja |
| Referrer-Policy | Controla qué URL de origen se envía | Baja |

Práctica de coaches (Juan): en WordPress se mejoran con un plugin de seguridad; para revisarlas, securityheaders.com. `scripts/chequeos_tecnicos.py` las comprueba por plantilla.

## 3. Cadenas de redirección

- Máximo **1 salto**. Si A va a B y B va a C, cambia A para que vaya directo a C (coincide con Juan: "A a C y B a C, no A a B a C").
- 301 para movimientos permanentes. Un 302 que parece permanente es un hallazgo medio.
- Revisa también bucles y el salto `http://` a `https://` del dominio.
- Después de una migración, actualiza los enlaces internos para que no pasen por la redirección.

## 4. Renderizado JavaScript (SSR vs CSR)

Esta parte sí está en el diplomado: Semana 3 · "Cómo funciona Google" (el renderizado como tercera etapa, "elegir bien entre SSR o CSR para no ocultar información") y la práctica de Juan (ver código fuente, Ctrl+F con un texto visible; si no aparece, es CSR). Lo que añade claude-seo, como casos límite:

1. Si el canonical del HTML crudo difiere del que inyecta JavaScript, Google puede usar cualquiera: que sean idénticos.
2. Si el HTML crudo trae `noindex` y el JavaScript lo quita, Google puede respetar el `noindex` del crudo. Sirve las directivas correctas en la respuesta inicial.
3. Google no renderiza JavaScript en páginas que responden con un código distinto de 200.
4. Datos estructurados inyectados por JS pueden procesarse con retraso. En fichas de producto, ponlos en el HTML del servidor.
5. Googlebot lee los primeros **2 MB de HTML**. Base64 en línea, CSS/JS en línea enormes o menús pesados pueden dejar fuera el contenido o el JSON-LD.

Prueba rápida: `python3 scripts/chequeos_tecnicos.py URL --texto "una frase visible"`.

## 5. Paginación

Alineado con la práctica de coaches (Juan): una URL paginada no se autocanoniza; lleva canonical a la página principal del listado y, según el caso, `noindex`. Añade la comprobación de que `rel="next/prev"` ya no lo usa Google (puedes dejarlo, no aporta). Para "cargar más" con JavaScript, comprueba que cada página tenga URL propia enlazada con `<a href>`.

## 6. Rastreadores de IA y robots.txt

El tema vive en la skill `sitemap-y-robots` (sección de bots de IA). Resumen: bloquear `Google-Extended` no afecta a Google Search ni a AI Overviews; `GPTBot` es entrenamiento y `ChatGPT-User` es navegación en tiempo real; Cloudflare puede inyectar reglas que bloquean bots de IA sin que el sitio lo sepa.

## 7. Rúbrica de severidad y puntaje de salud

Severidades de la skill (las mismas del dashboard): **Crítico** (bloquea rastreo o indexación de plantillas enteras, o rompe HTTPS), **Alto** (afecta a una plantilla importante o a muchas URLs con impacto claro), **Medio**, **Bajo-Medio**, **Bajo** (higiene). Criterio práctico de coaches: botones rotos, H1 e imágenes pesadas son prioridad alta; la falta de alt es baja.

`scripts/puntaje_salud.py issues.json` resume todo en un número de 0 a 100 con una rúbrica propia (resta por severidad con tope). Úsalo solo para comparar una auditoría con la anterior. No es una métrica de Google; no lo presentes al cliente como tal.

## 8. Comparar corridas (antes y después)

Idea tomada de `seo-drift`: guarda la salida de `onpage_extract.py` como línea base y compárala con la siguiente corrida. `scripts/comparar_corridas.py anterior.json actual.json` marca como **críticos** un `noindex` nuevo, un canonical eliminado o cambiado, un H1 o title eliminado y un status que pasa de 2xx a 4xx/5xx. Encaja con el reporte mensual "mes actual vs mes anterior" de la Semana 12 · "¿Cómo hacer un reporte SEO?". No se creó una skill aparte porque el diplomado no enseña un monitoreo de elementos de página (ver changelog).

## 9. Otros scripts de claude-seo que puedes consultar

`fetch_page.py` (descarga con control de redirecciones), `consistency_check.py` (coherencia title/H1/canonical), `indexnow_submit.py` (avisar a Bing/Yandex de URLs nuevas; Google no usa IndexNow) y `sitemap_discovery.py`. Aquí solo se portó lo imprescindible en stdlib. IndexNow envía URLs a un tercero: pide permiso al usuario antes de usarlo.
