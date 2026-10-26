# Complementos de claude-seo para metas y on-page

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.** Origen: `skills/seo-content-brief/SKILL.md` (sección Meta Tag Rules) y `references/keyword-density.md`. Adaptado al español. Si algo contradice al curso, gana el curso.

## 1. Umbrales de metas: diferencias
| Elemento | claude-seo | Diplomado (se aplica) |
|---|---|---|
| Meta título | 50 a 60, keyword al inicio, marca al final separada por barra o guion, adelantar resultados, números o datos concretos | 50 a 60, keyword al inicio |
| Meta descripción | 130 a 150, voz activa, amplía el título con ventajas y datos, termina con CTA, **sin marca al final** y **sin comillas** (Google trunca en las comillas) | 120 a 155, persuasiva, con CTA |
Aplica el rango del curso. Del complemento sí vale como práctica: no poner comillas dobles dentro de la descripción, no repetir la marca si ya está en el título, y abrir el título con un resultado o dato concreto cuando se pueda.

## 2. Colocación de la keyword principal
Debe aparecer en meta título (cerca del inicio), H1, URL, meta descripción, primer párrafo y al menos un Alt Text. No es necesaria en cada H2/H3 ni en cada anchor. Un H1 más una o dos apariciones en H2 bastan. Se alinea con S8 L5 y S11 L2.

## 3. Severidad para auditorías masivas de metas
Rúbrica del script `scripts/meta_audit.py` (criterio propio, inspirado en las auditorías por plantilla):
- **Alta:** meta faltante o duplicada entre URLs.
- **Media:** fuera de rango (50 a 60 o 120 a 155).
- **Baja:** keyword que no está al inicio del título.
Si el patrón se repite, corrige la plantilla del CMS antes que URL por URL (Rank Math, Yoast).

## 4. Ideas que no se trajeron
- Reglas de títulos "con números y poder" de herramientas de CTR: no hay base en el curso; las variantes A/B ya cubren ángulos (beneficio, número, urgencia, pregunta del PAA).
