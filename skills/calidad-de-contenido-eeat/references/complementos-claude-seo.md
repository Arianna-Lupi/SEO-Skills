# Complementos de claude-seo para calidad de contenido

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.** Autor: agricidaniel. Origen: `skills/seo-content/SKILL.md`, `agents/seo-content.md`, `scripts/content_quality.py`, `scripts/content_humanize.py`, `scripts/content_verify.py`. Adaptado al español. Si algo contradice al curso, gana el curso.

## 1. Prueba Quién / Cómo / Por qué (heurística de Google)
Antes de revisar los 4 pilares, pasa la pieza por tres preguntas basadas en la guía de contenido útil de Google:
| Pregunta | Qué buscar |
|---|---|
| **Quién** lo creó | Firma visible, bio, credenciales. Indispensable donde el lector lo espera, y obligatorio en temas sensibles. |
| **Cómo** se creó | Transparencia del proceso cuando el lector lo preguntaría razonablemente, sobre todo si hubo IA. Evidencia de primera mano, investigación propia. |
| **Por qué** existe | Para ayudar a las personas, no para atraer clics. Cuidado con entrar a un nicho sin experiencia, publicar por frescura o escribir para llegar a un número de palabras. |
Si las tres respuestas son débiles, la pieza está en riesgo. Encaja con Confiabilidad (S7 L5) y valor real (S11 L2).

## 2. Rúbrica con pesos internos
claude-seo puntúa de 0 a 100 con pesos propios: Experiencia 20, Especialización 25, Autoridad 25, Confiabilidad 30 (la confianza pesa más, en línea con el curso). **Google no publica pesos numéricos:** son un modelo interno de esa herramienta. En esta skill no usamos nota numérica; la rúbrica de `rubrica-revision.md` usa OK, Ajustar y Falla. Si el cliente pide una nota, preséntala como heurística y nunca como dato de Google.

## 3. Suelos de cobertura por tipo de página (solo orientativos)
Home 500, servicio 800, blog 1.500, producto 300 o más (400 o más si es complejo), ubicación 500 a 600 palabras. claude-seo aclara que **son pisos de cobertura, no objetivos, y que el conteo de palabras no es factor de ranking**. El curso no fija longitudes y la práctica de coaches desaconseja perseguir una cifra, así que el script solo emite una alerta **baja** si estás por debajo.

## 4. Legibilidad
Objetivo orientativo de Flesch 60 a 70 y frases de 15 a 20 palabras en promedio, párrafos de 2 a 4 frases. claude-seo aclara que **Flesch no es un factor de ranking**. El curso fija párrafos de 3 a 4 líneas y usa Hemingway como filtro (S11 L4). Para español, el índice Flesch original no está calibrado; usa el criterio del curso y el juicio humano.

## 5. Detección de contenido genérico de IA (origen: content_quality.py y content_humanize.py)
Marcas de contenido de baja calidad: frases genéricas sin especificidad, ninguna idea original, estructura repetida entre páginas, sin autoría, errores factuales. Las guías de evaluadores de Google miran patrones de contenido escalado, copiado o generado sin valor, **no la autoría por IA en sí**. El script `redaccion-y-optimizacion-nlp/scripts/ai_tells.py` es una adaptación al español y **no emite veredicto**.
Checklist anti contenido genérico (aplícalo después de la humanización del curso):
1. ¿Hay al menos 3 puntos con opinión, anécdota o dato propio?
2. ¿Cada afirmación con cifra tiene fuente cercana?
3. ¿Las introducciones y cierres dicen algo concreto, o son frases comodín?
4. ¿Las aperturas de frase y de sección varían?
5. ¿Hay ejemplos del sector, de la ciudad o del cliente real?
6. ¿El texto se podría pegar en otra web del mismo nicho sin cambiar nada? Si sí, falta valor propio.

## 6. Verificación de afirmaciones (origen: content_verify.py)
Detecta afirmaciones verificables (estadísticas, cifras grandes, "según un estudio", fechas, comparaciones) y marca las que no tienen una fuente cerca (enlace, nota al pie o atribución). Es la versión automática del fact-checking de S14 L12; el script `calidad_contenido.py` incluye una versión simple.

## 7. Citabilidad y Google (matiz importante)
claude-seo cita guías oficiales de Google según las cuales optimizar para funciones de IA generativa **es SEO** y no requiere archivos ni marcado especial, y avisa de que ninguna herramienta garantiza posicionamiento. El curso (S14 L13) enseña técnicas de citabilidad (respuesta directa, listas, tablas, FAQ Schema). Decisión: aplica las técnicas del curso porque también mejoran la lectura, y **no vendas la citabilidad como garantía** de aparecer en respuestas de IA. Sobre FAQ Schema, ver la nota en `actualizacion-de-contenido/references/complementos-claude-seo.md` (sección 6).

## 8. Frescura
Fecha de publicación visible; fecha de actualización si se revisó; revisa lo que tenga más de 12 meses en temas que cambian rápido.

## Ideas que no se trajeron
- Puntuación "AI Citation Readiness 0 a 100": no hay base en el curso ni método reproducible; se resuelve con el apartado 6 de la rúbrica.
- Auditoría de enlaces externos y backlinks para "autoridad": es otra skill (`auditoria-de-backlinks-toxicos`) y requiere datos reales.
