# Complemento externo (claude-seo, MIT), no es parte del método del diplomado

> Origen: `claude-seo` de agricidaniel (licencia MIT), `skills/seo-cluster/references/hub-spoke-architecture.md` (reglas anti canibalización y cuadro de mando del cluster) y `skills/seo-sxo/` (desajuste de página con la SERP). Adaptado al español. Si algo de aquí contradice el diplomado, **gana el diplomado** (Semana 5).

Úsalo solo **después** de terminar el mapa con el método de Verónica.

## 1. Rúbrica de Valor SEO por URL (ayuda para casos dudosos)

El diplomado usa una pregunta test: "¿un usuario buscaría esto en Google?" (Semana 5 · lección 4). Para URLs dudosas, puntúa estas señales con Sí o No y decide:

| Señal | Sí suma |
|---|---|
| Responde a una intención de búsqueda clara | +1 |
| Hay demanda visible (la SERP muestra más de 3 artículos o más de 5 páginas sobre el tema, criterio de Vero) | +1 |
| Ayuda a convertir o a mover al usuario hacia una página que convierte | +1 |
| Tiene contenido propio y suficiente (no es un listado automático ni una página casi vacía) | +1 |
| Cumple una función en la estructura (pilar, categoría, soporte de un cluster) | +1 |

Lectura: 4 o 5 señales, Valor SEO = Sí y candidata a Top 5 si además tiene intención alta. 2 o 3, Sí con prioridad baja o Unificar con otra. 0 o 1, Valor SEO = No (Eliminar o Redireccionar si ensucia el rastreo). Es una ayuda para decidir y no sustituye el criterio del curso.

## 2. Reglas anti canibalización al planificar (contraste)

- Dos URLs no comparten keyword primaria. Después de asignar, lista todas las keywords primarias y busca casi duplicados ("mejor CRM" y "top software CRM").
- Si hay casi duplicados, une las páginas o diferéncialas por intención (por ejemplo una lista de los mejores y una comparativa).
- Si el solape de SERP entre dos keywords es muy alto (7 o más URLs de 10), una sola página. Ver `../../intencion-de-busqueda/references/complementos-claude-seo.md`.

## 3. Comprobaciones de calidad del mapa (inspiradas en el cuadro de mando de claude-seo)

El cluster de claude-seo lleva un cuadro con cobertura, enlazado, huérfanas, canibalización y huecos de contenido. Para el mapa, `scripts/validar_mapa.py` revisa de forma parecida: completitud (URLs con valor que tienen keyword, temperatura y acción), canibalización planificada, páginas técnicas con valor SEO y acciones incoherentes con la posición. El `map_score` es una convención de este repo.

## 4. Desajuste página y SERP

Si una URL con keyword asignada tiene un formato distinto al que premia la SERP (artículo frente a categoría, por ejemplo), no sigas optimizándola: reasigna la keyword o cambia el formato. Usa la skill `intencion-de-busqueda`.
