# Complementos de claude-seo para el reporte SEO

> **Complemento externo (claude-seo, MIT, agricidaniel), no es parte del método del diplomado.** El diplomado reporta con **Search Console** (4 métricas) y menciona Analytics solo como herramienta aparte (S3 L11). Lo de abajo suma datos opcionales sin cambiar la estructura del informe.

## Core Web Vitals de campo (CrUX)

Los datos de **campo** son de usuarios reales (percentil 75, últimos 28 días); los de **laboratorio** (Lighthouse, skill `analisis-rendimiento`) son una simulación. Cuando el cliente pregunta "¿pasamos Core Web Vitals?", responde con campo.

`scripts/crux_campo.py` (stdlib) consulta la CrUX API con una clave gratuita (`CRUX_API_KEY`) y deja `.seo-audit/<sitio>/data/cwv-field.json`. Umbrales de Google, bueno / pobre: LCP 2.500 / 4.000 ms, INP 200 / 500 ms, CLS 0,1 / 0,25. Se aprueba si LCP, INP y CLS están en "bueno" en p75. Si CrUX no tiene datos (poco tráfico), el informe dice **pendiente de dato**; no se estima. Alternativa manual: sección "Datos de campo" de PageSpeed Insights o informe Core Web Vitals de GSC.

## Datos de GSC por API

claude-seo trae `gsc_query.py` (consultas por fecha, página, país, dispositivo) y `gsc_inspect.py`, con OAuth o cuenta de servicio. No se portaron: requieren `requests` y autenticación de Google; el flujo del diplomado (exportar de la interfaz de GSC o usar `mcp-gsc`) cubre el informe. Útil saber: la API permite más de 1.000 filas, el export de la interfaz no.

## Analytics (GA4) como contexto

Opcional: sesiones orgánicas y conversiones desde GA4 para el KPI de negocio (S12 L6: KPIs vs métricas de apoyo). No mezcles GA4 con las 4 métricas de GSC en la misma tabla; sepáralas y cita la fuente.

## Estructura de salida

claude-seo propone reportes PDF/HTML con gráficas (`google_report.py`). Esta skill mantiene el formato del diplomado (Doc con Resumen Ejecutivo, Rendimiento mes vs mes, Ganadoras, Tareas y Próximos Pasos). El dashboard local (`dashboard-seo`) muestra las mismas cifras desde `search-console.json`.

## Descartado

- Indexing API, Keyword Planner y Google Ads: fuera del diplomado.
