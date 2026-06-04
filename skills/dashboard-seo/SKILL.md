---
name: dashboard-seo
description: Usa esta skill como PASO DE CIERRE de cualquier trabajo SEO para entregar un dashboard local con TODO lo encontrado, o cuando el usuario pida ver los resultados juntos — aunque no diga "dashboard", p.ej. "muéstrame todo junto", "un panel con los resultados", "informe visual", "una web local con la auditoría", "el resumen de todo". Reúne en una sola página local (issues por severidad, keywords, las 10 de Oro, clusters, competidores, AEO/GEO, auditorías previas, inventario y próximos pasos) los datos estructurados que las skills y agentes dejan en .seo-audit/<sitio>/data/*.json, genera el index.html y devuelve un URL local (http://127.0.0.1:PUERTO). Es el entregable final: cualquier auditoría, investigación de keywords o flujo de contenido debe terminar aquí.
compatibility: Script requiere Python 3 (uv), solo stdlib. Sirve con `python3 -m http.server`. No necesita claves ni red. La carpeta .seo-audit/ va en .gitignore (datos del cliente, no se suben).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> El dashboard solo muestra lo que está en los `data/*.json`. Si un dato no existe (GSC, volumen/KD, Core Web Vitals…), NO lo inventes: déjalo fuera o márcalo en `meta.json → pending_data` como pendiente. Mejor una sección honesta vacía que una cifra falsa.

# Dashboard SEO (entregable de cierre)

Actúa como el integrador final en aprendoseo. Tu trabajo: tomar todo lo que produjeron las demás skills y agentes y entregar **una sola web local** que el usuario abre en el navegador y ve todo de un vistazo: issues, keywords, clusters, competidores, búsqueda con IA, auditorías y próximos pasos. **Todo flujo SEO termina aquí.**

## Convención de datos (dónde escribe cada skill/agente)

Carpeta por proyecto, **gitignored** (datos del cliente, no se suben):

```
<repo>/.seo-audit/<sitio>/
  data/                      ← cada skill/agente deja su salida estructurada aquí
    meta.json                resumen global: {site, owner?, repo?, stack?, market?, generated,
                               summary:{urls,issues_total,issues_critical,issues_high,
                               keyword_candidates,golden_keywords,clusters,prior_audits,...},
                               data_sources:[...], pending_data:[...]}
    issues.json              {issues:[{id,title,severity("Crítico|Alto|Medio|Bajo-Medio|Bajo"),
                               block,fix,status,evidence,verified(true|"parcial"|"doc"|"no confirmado"),
                               github?}], counts:{...}}   ← auditoria-tecnica
    keywords.json            {candidates:[{keyword,seed,source,intent,volume,kd}], golden:[{kw,cluster,why}], note}
                               (volume/kd = "pendiente" si no hay export real)   ← investigacion-de-keywords
    clusters.json            {clusters:[{pilar,url,spokes:[]}]}   ← estrategia-de-contenidos-clusters
    competitors.json         {by_pillar:[{pillar,query,results:[{position,domain,title,url}]}], strategic:[]}
                               ← analisis-serp-y-competencia
    ai-features.json         {queries:[{query,ai_overview,featured_snippet,paa,recommendation}]}   ← optimizacion-geo-aeo
    content-briefs.json      {briefs:[{keyword,type,url,meta_title,angle,status}]}   ← brief-de-contenido / redaccion
    prior-audits.json        {audits:[{name,score,date,summary,file}]}
    inventory-summary.json   {total_urls,source,http_sample,note}   ← inventario-de-urls
    next-steps.json          {steps:[{prio,area,action,impact,effort}]}
  index.html                 ← lo genera build_dashboard.py
```

Reglas:
- **Funciona con lo que haya.** No hace falta tener todos los archivos: las secciones sin datos se ocultan solas.
- Cada skill, al terminar su trabajo para un sitio, **escribe/actualiza su JSON** en `data/` (con `Write` o su script). No pisa los de las demás.
- Los valores que no son reales van como `"pendiente"` y/o se listan en `meta.pending_data`.

## Proceso

1. **Confirma el sitio** (dominio) y la raíz del repo/proyecto.
2. **Verifica que el `.gitignore` ignore `.seo-audit/`**; si no, añádelo (esos datos son del cliente).
3. **Asegúrate de que `data/*.json` tengan lo que produjeron las skills/agentes** de esta sesión. Si falta algo clave que sí se generó, persístelo antes de seguir.
4. **Genera el dashboard:**
   ```bash
   uv run build_dashboard.py --site <sitio>
   ```
   Devuelve `{ok, dir, index, url, serve_cmd}`.
5. **Sírvelo** (en segundo plano) y **entrega el URL** al usuario:
   ```bash
   python3 -m http.server 8787 --bind 127.0.0.1 --directory <dir>
   ```
   (o `uv run build_dashboard.py --site <sitio> --serve` para servir en primer plano).
6. **Responde con el URL local** (`http://127.0.0.1:8787/`) + un resumen de 2-3 líneas de lo más importante (críticos, próximos pasos) y qué quedó `pendiente de dato`.

## Salida

Un URL local navegable con todo lo encontrado, datos estructurados persistidos en `data/*.json`, y el recordatorio de qué falta (sin inventar nada).

## Ejemplo

Tras correr `agente-auditoria-tecnica` + `agente-investigacion-keywords` sobre `ejemplo.com`:
1. Los agentes dejaron `issues.json`, `keywords.json`, `clusters.json`, `competitors.json` en `.seo-audit/ejemplo.com/data/`.
2. `uv run build_dashboard.py --site ejemplo.com` → genera `index.html`.
3. `python3 -m http.server 8787 --directory .seo-audit/ejemplo.com` (background).
4. Respondes: *"Dashboard listo: http://127.0.0.1:8787/ — 1 crítico (sitemap), 2 altos. Pendiente: conectar GSC y volumen/KD."*

## Script determinista (ahorro de tokens)

`scripts/build_dashboard.py` — lee `.seo-audit/<sitio>/data/*.json`, escribe `index.html` (página autocontenida, sin dependencias) y opcionalmente sirve con `--serve`. Oculta secciones sin datos. Stdlib pura.
