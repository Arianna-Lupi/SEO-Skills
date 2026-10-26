# Complemento externo (claude-seo, MIT), no es parte del método del diplomado

> Origen: `claude-seo` de agricidaniel (licencia MIT), `skills/seo-cluster/` (`references/serp-overlap-methodology.md` y `hub-spoke-architecture.md`). Adaptado al español. Si algo de aquí contradice el diplomado, **gana el diplomado** (Semana 4 · lecciones 11, 13 y 14).

Úsalo solo **después** de agrupar a mano en clusters (paso 5 del `SKILL.md`) y como contraste.

## 1. Agrupar por solape de SERP en vez de por parecido de texto

El diplomado agrupa por tema (Semana 4 · lección 11). Para decidir si dos keywords de un mismo cluster merecen **páginas distintas**, compara sus top 10:

- Muchas URLs en común (7 o más de 10): intención compartida, una sola página. Gana la keyword de mejor ratio volumen/dificultad (es el Duelo de Keywords aplicado a la SERP).
- Solape medio (4 a 6): mismo cluster, decide entre páginas separadas o secciones según volumen y formato.
- Solape bajo (2 a 3): clusters vecinos que se enlazan. Solape casi nulo (0 a 1): temas separados.

Ejecuta `../../intencion-de-busqueda/scripts/serp_overlap.py` con las SERP capturadas. Explicación completa y cautelas en `../../intencion-de-busqueda/references/complementos-claude-seo.md`.

## 2. Pregrupación para listas grandes

Con más de 40 keywords no compares todas contra todas. Agrupa antes por intención y por término principal, compara solo dentro del grupo y revisa por muestreo unos cuantos pares que dejaste fuera. Mantén un registro de las SERP ya consultadas para no repetir búsquedas.

## 3. Tamaño orientativo de un cluster al planificar (idea externa)

claude-seo sugiere de 2 a 5 clusters por pilar y de 2 a 4 posts por cluster al empezar. El diplomado pide 3 a 4 clusters iniciales y calendario según capacidad (Semana 7 · "10 de Oro"); usa el del diplomado y toma esto solo como contraste.
