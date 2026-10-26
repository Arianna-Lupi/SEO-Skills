# Comandos de competencia, GEO y off page

## `/aprendoclub competitors <keyword o sitio>`

- **Ejecuta** (Semana 6), en este orden:
  1. `analisis-serp-y-competencia`: Competidor de Negocio vs Competidor SEO, Ojo Clínico sobre el top 3 (manual, primero), y luego los aceleradores:
     - `serp.py "<keyword>"` trae el top orgánico, PAA y features (SerpApi, con confirmación).
     - `perfil_competidor.py --serp-json <serp.json> --own-url <tu-url>` perfila cada página del top (también acepta URLs sueltas o `--html` sin red).
     - `comparar_serp.py <perfiles.json> --sitio <sitio> --md informe.md` compara con tu página: patrón común, brechas, puntaje de Costo de Oportunidad (puntaje relativo, no del diplomado), Análisis de Repetición y tareas con ICE. Escribe `competitors.json`.
  2. `analisis-de-competidores`: dominios por Análisis de Repetición (`competitor_domains.py`).
- **Sitio sin keyword:** pide 3 a 5 keywords del negocio o toma las de `keywords.json`.
- **Ejemplo:** `/aprendoclub competitors "comprar café de especialidad"`
- **Salidas:** `competitors.json` (con `by_pillar`, `strategic` y `serp_analysis`), informe en Markdown.
- **Datos:** el volumen real se pasa con `--volumenes`; sin él queda `pendiente de dato`. Las páginas que dependen de JavaScript se marcan, no se renderizan.

## `/aprendoclub geo <url>`

- **Ejecuta:** `optimizacion-geo-aeo` (Semanas 14 y 16): features de IA de la SERP (`ai_features.py`), rastreadores de IA y robots (`ai_crawlers.py`), estructura citable y presencia de marca.
- **Ejemplo:** `/aprendoclub geo https://midominio.com`
- **Salidas:** `ai-features.json`.
- **Nota:** `llms.txt` es opcional y Google Search no lo usa; no se promete efecto.

## `/aprendoclub backlinks <sitio>`

- **Ejecuta:** `auditoria-de-backlinks-toxicos`: clasifica dominios en Toxic, Suspicious, Low-quality-but-safe y Neutral-OK, y genera `disavow.txt`. Solo si el usuario pide construir enlaces nuevos, sigue con `link-building-y-outreach` (primero limpia, después construye).
- **Datos:** export de backlinks (Ahrefs u otro). Sin export, `pendiente de dato`. El archivo `disavow.txt` se entrega, no se sube a Search Console sin que el usuario lo decida.
- **Ejemplo:** `/aprendoclub backlinks midominio.com`
- **Salidas:** `backlinks.json`, `domain-classification.csv`, `disavow.txt`.
