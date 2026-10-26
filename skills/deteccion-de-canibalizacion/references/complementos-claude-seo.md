# Complemento externo (claude-seo, MIT), no es parte del método del diplomado

> Origen: `claude-seo` de agricidaniel (licencia MIT), `skills/seo-cluster/SKILL.md` y `references/hub-spoke-architecture.md` (regla de canibalización: ningún par de URLs comparte keyword primaria; solape de SERP alto implica fusionar) y `references/serp-overlap-methodology.md`. claude-seo trata la canibalización como prevención al planificar clusters, no como diagnóstico con datos de Search Console; lo de abajo combina esa idea con la práctica de este repo. Si algo contradice el diplomado, **gana el diplomado**.

## 1. Matriz de decisión ampliada

Después de ver los datos de GSC, decide con tres preguntas y no con una sola:

| ¿Misma intención (SERP casi igual)? | ¿Contenido muy parecido? | Decisión |
|---|---|---|
| Sí | Sí | Fusionar en la URL ganadora y 301 de la débil |
| Sí | No (ángulos distintos) | Unificar el tema en una URL con secciones; la otra se redirige o se convierte en soporte con otra keyword |
| No | Sí | Diferenciar: retitular, cambiar la keyword de la débil, reforzar enlaces al pilar |
| No | No | No es canibalización; monitoriza |

La SERP la mides con `intencion-de-busqueda/scripts/serp_overlap.py`: 7 o más URLs compartidas en el top 10 indican misma intención (umbral externo, ver su complemento).

## 2. Cómo elegir la URL ganadora

Prioriza, en este orden y con datos reales: más clics en el periodo, mejor posición media, más enlaces internos y externos, mejor coincidencia con el formato que premia la SERP, más reciente. Redirige siempre la débil hacia la fuerte. No inventes enlaces entrantes: usa Ahrefs o GSC.

## 3. Plan de redirecciones y enlazado

- Lista las URLs a redirigir con su destino 301 y el motivo.
- Actualiza los enlaces internos para que apunten a la URL final y no a la redirigida (evita cadenas).
- Conserva en la URL ganadora las secciones valiosas de la débil antes de redirigir.
- Revisa el canonical de ambas y quita la débil del sitemap.

## 4. Medición posterior

Vuelve a exportar GSC 4 a 8 semanas después de aplicar el cambio y compara: queries que dejaron de repartirse, posición de la URL ganadora y clics totales de la query. Con tiempos y cifras reales; si no hay datos suficientes, repórtalo como `pendiente de dato`.

## 5. Prevención en cada alta de contenido

Antes de publicar una URL nueva, comprueba que su keyword primaria no figura en el mapa y que no es casi duplicada de otra ("mejor CRM" y "top software CRM"). `mapa-de-palabras-clave/scripts/validar_mapa.py` hace esa comprobación.
