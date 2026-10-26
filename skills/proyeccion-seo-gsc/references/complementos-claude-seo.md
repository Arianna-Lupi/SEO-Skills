# Complementos: proyección con Search Console

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.** Origen: `skills/seo-google`, `scripts/google_report.py`, `scripts/gsc_query.py` y `skills/seo-plan` de agricidaniel/claude-seo.

- claude-seo trae las consultas y páginas de Search Console por API (`gsc_query.py`) y arma reportes con datos de Google (`google_report.py`). Es una forma de obtener los exports que esta skill consume; en este repositorio el equivalente es el MCP de GSC o el export manual.
- Su planificación (`seo-plan`) incluye una tabla de KPI con base, 3, 6 y 12 meses, pero **sin método de cálculo** ni proyección. No se importó ninguna proyección de claude-seo: no había fórmulas verificables.
- Las curvas de CTR por posición publicadas por terceros varían mucho por sector y tipo de consulta. Por eso esta skill calcula la curva de la propia web y, si no hay muestra, exige que el usuario aporte una y la rotula como supuesto.
