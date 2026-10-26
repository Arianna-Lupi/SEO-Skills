# Complementos de claude-seo para redacción y optimización

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.** Autor: agricidaniel. Origen: `skills/seo-content/SKILL.md`, `skills/seo-content-brief/references/keyword-density.md`, `scripts/content_quality.py`, `scripts/content_humanize.py`. Adaptado al español. Si algo contradice al curso, gana el curso.

## 1. Colocación de la keyword principal (sin cuota de densidad)
Revisa que aparezca de forma natural en meta título, H1, URL, meta descripción, primer párrafo y al menos un Alt Text. No la repitas en cada H2, párrafo o anchor. El curso lo resume como "keyword en H1 y primeras 100 palabras, natural" (S11 L2). claude-seo suele citar 1 a 3 % de densidad, pero **lo declara una heurística de lectura, no una regla de Google**; el script `readability.py` reporta el porcentaje solo como alerta de relleno.
Errores frecuentes: obsesión por la coincidencia exacta, keyword en todos los H2, olvidar el Alt Text, contar sinónimos como densidad.

## 2. Términos secundarios y semánticos
Referencia: 5 a 8 términos cercanos repartidos por el cuerpo y los H2 a H6, y 10 a 15 términos semánticos más amplios. Es la versión cuantificada de "optimiza entidades, no la repetición" (S11 L5). Usa DinoRank, Surfer o Neuron Writer (curso) para obtenerlos; el número es orientativo.

## 3. Checklist anti contenido genérico de IA
Después de la humanización del curso, comprueba:
1. ¿Hay al menos 3 puntos con opinión, anécdota o dato propio?
2. ¿Cada cifra o estudio tiene fuente cercana?
3. ¿Las introducciones y cierres dicen algo concreto?
4. ¿Las aperturas de frase y de sección varían?
5. ¿Hay ejemplos del sector, ciudad o cliente real?
6. ¿Podrías pegar el texto en otra web del nicho sin cambiar nada? Si sí, falta valor propio.
7. ¿Queda alguna raya larga, "sumérgete", "en el mundo actual" o frase comodín?
Automatízalo con `scripts/ai_tells.py` (adaptado al español de `content_humanize.py` y `content_quality.py`, que son para inglés). **No es un detector de autoría:** señala pistas para editar. Las guías de calidad de Google miran contenido escalado, copiado o sin valor, no que haya participado una IA.

## 4. Legibilidad
Referencias: frases de 15 a 20 palabras en promedio, párrafos de 2 a 4 frases. **Flesch no es factor de ranking**, y su fórmula original no está calibrada para español; mantén el criterio del curso (párrafos de 3 a 4 líneas, Hemingway como filtro).

## 5. Estructura
Tabla de contenidos para piezas largas; tablas y listas para datos comparativos; respuesta directa de 40 a 60 palabras al inicio para apuntar a fragmentos destacados (coincide con S14 L13: menos de 40 palabras en el primer párrafo).

## 6. Enlazado y fuentes
Referencia de 3 a 5 enlaces internos por cada 1.000 palabras con anchor descriptivo; cita fuentes de autoridad. El curso define los enlaces desde el brief (From y To); esta cifra es solo una referencia de densidad.

## Ideas que no se trajeron
- Reescritura automática de frases (`content_humanize.py` las sustituye 1 a 1): en el curso la humanización la hace la persona con su experiencia (S11 L3, S14 L12), así que el script solo señala.
