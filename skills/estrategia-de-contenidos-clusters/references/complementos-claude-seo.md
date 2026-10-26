# Complementos de claude-seo para clusters y estrategia

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.** Autor: agricidaniel; autora original del método de clustering por SERP: Lutfiya Miller. Origen: `skills/seo-cluster/SKILL.md` y `references/serp-overlap-methodology.md`, `hub-spoke-architecture.md`. Adaptado al español. Si algo contradice al curso, gana el curso.

## 1. Agrupar por solapamiento real de SERP
Principio: **dos keywords que devuelven casi las mismas URLs deben resolverse con la misma página; si sus SERP son distintas, necesitan páginas distintas.** Sirve para decidir con evidencia cuando el curso dice "decide según la intención o elige el cluster con menos contenido" (S7 L3) y para detectar canibalización antes de producir.
Cuenta cuántas URLs del top 10 comparten dos keywords (ignora anuncios, fragmentos y PAA):
| URLs compartidas | Relación | Qué hacer |
|---|---|---|
| 7 a 10 | Misma página | Fusiona; la de mayor volumen es la principal |
| 4 a 6 | Mismo cluster | Páginas distintas del mismo tema |
| 2 a 3 | Enlazar | Clusters vecinos con enlaces cruzados |
| 0 a 1 | Separadas | Otro cluster o fuera del tema |
Desempate en 3 a 4: dominios coincidentes, misma intención, relación de volumen (si una tiene 10 veces más, merece su propia página); en duda, mismo cluster con páginas separadas. Los umbrales son valores de partida de claude-seo, no reglas de Google.
Script incluido: `scripts/serp_overlap.py`. **No consulta ninguna SERP:** le pasas las URLs que obtuviste con SerpApi, Ahrefs o a mano.

## 2. Reducir comparaciones
Con 40 keywords hay 780 pares. Agrupa primero por intención o por palabra cabeza y compara solo dentro del grupo más las keywords de frontera. Variantes de cola larga de la misma cabeza y misma intención se asumen mismo cluster y se verifican con una muestra.

## 3. Anti patrones
1. No agrupar solo por parecido de texto ("entrenamiento de perros" y "clases de adiestramiento" pueden tener SERP distintas).
2. No agrupar solo por raíz de palabra.
3. No asumir que las búsquedas relacionadas pertenecen al mismo cluster sin verificar.
4. No ignorar diferencias de funciones de SERP: un mapa local frente a un fragmento destacado suele pedir otro tipo de contenido.
5. No tratar igual a todos los dominios: quita los que aparecen en todas las SERP (Wikipedia, YouTube, marketplaces) antes de contar (`--ignorar-dominios`).

## 4. Estructura pilar y spokes: referencias
claude-seo propone 2 a 5 clusters por pilar, 2 a 4 spokes por cluster, longitudes de 2.500 a 4.000 palabras para el pilar y 1.200 a 1.800 para los spokes, y reglas de enlazado: todo spoke enlaza al pilar y el pilar a cada spoke; 2 a 3 enlaces entre spokes del mismo cluster; 0 a 1 entre clusters; mínimo 3 enlaces entrantes por post; cero huérfanas y todo a 2 clics del pilar. **El curso no fija longitudes ni cantidad de spokes:** usa solo las reglas de enlazado como lista de control (regla de 3 clics, S9). Para el diseño de la arquitectura usa `arquitectura-y-enlazado-interno`.

## 5. Tablero de control del cluster (adaptado)
| Métrica | Meta |
|---|---|
| Cobertura (piezas escritas / planeadas) | 100 % |
| Enlaces internos por pieza | 3 o más |
| Huérfanas | 0 |
| Canibalización (misma keyword principal en dos piezas) | 0 |
| Spokes que enlazan al pilar y viceversa | 100 % |
Es una lista de control, no un puntaje de Google.

## 6. Páginas por ciudad y SEO programático (idea descartada como skill)
El diplomado no enseña SEO programático. Lo más cercano: SEO Local (Semana 14, lección 2), "[Servicio] en [Ciudad]" y landings por localidad (práctica de Diana #61, #62, #153), y la nota de Juan sobre carpetas por ciudad con una keyword base como formato apto para programático. claude-seo tiene `skills/seo-programmatic`, pero **no se creó skill** porque no hay lección del curso que la respalde. Mientras tanto, para landings locales: una página por ubicación con contenido genuinamente distinto (intención, estructura y datos locales), no una plantilla con la ciudad cambiada.
