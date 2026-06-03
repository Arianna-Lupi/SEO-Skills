# Método del diploma — Optimización GEO / AEO para la búsqueda con IA (Semanas 14 y 16)

> Fuente: corpus interno "De Cero a SEO" (chunks, doc_type resumenes-prompts/transcripciones), Semanas 14 y 16. Material de aprendoseo.

Dos clases enseñan este tema, con instructores distintos:

- **Semana 14, clase 13 — "¿Cómo optimizar tu contenido para aparecer en respuestas de la IA?"** (instructor: **Daniel Quintero**). Introduce el concepto de **AEO (Answer Engine Optimization)**.
- **Semana 16, clase 1 — "Clase especial SEO PARA LLMs"** (instructor: **Ibrahim Mogollón**). Cubre **GEO + AEO + LLM** ("la sopa de letras del futuro").

Honestidad sobre la cobertura: el corpus es **sólido pero conciso** en GEO/AEO — son dos clases de resumen, no un módulo extenso. Lo de abajo es lo que el curso realmente dice; no se ha añadido material externo.

## El método paso a paso (como lo enseña el curso)

### AEO — Semana 14, clase 13 (Daniel Quintero)

Definición del curso: "Ya no basta con aparecer en los 'enlaces azules' de Google; el objetivo ahora es ser **la fuente de información** que herramientas como ChatGPT, Gemini y los Google AI Overviews (SGE) utilizan para responder a los usuarios."

**Cómo funcionan las respuestas de IA (la IA busca información "digerible"):**

1. **Entidades y Relaciones:** "La IA no solo lee palabras, busca entender conceptos y cómo se relacionan entre sí."
2. **Fuentes de Confianza:** "Gemini y ChatGPT citan sitios que demuestran autoridad y una estructura de datos impecable."
3. **Formatos de Respuesta:** "La IA prefiere contenidos que ya vienen en formatos listos para ser 'copiados y pegados', como listas, tablas o definiciones directas."

**Técnicas para ser citado por la IA (verbatim):**

- **Respuestas Directas:** "El primer párrafo de tu contenido debe responder a la pregunta principal de forma clara y concisa (estilo diccionario)." → answer-first.
- **Uso de Listas y Tablas:** "Estructurar la información de manera que la IA pueda extraerla fácilmente."
- **Marcado de Datos Estructurados (Schema):** "Implementar el esquema de FAQ (Preguntas Frecuentes) es vital para que los motores de IA identifiquen qué preguntas estás resolviendo."

**El nuevo estándar de contenido (ultra-estructurado):** Texto Alt en imágenes (contexto visual para la IA), Brevedad y Claridad ("menos relleno y más precisión técnica"), y **E-E-A-T** (Experiencia, Autoridad y Confianza) — "la IA prioriza contenido que parece escrito por un experto real en el tema".

### GEO/AEO para LLMs — Semana 16, clase 1 (Ibrahim Mogollón)

"El ecosistema de búsqueda ha cambiado. Ahora existen los LLMs… y nuestra misión es que estas herramientas nos citen como **la fuente de verdad**."

**¿Cómo aparecer en las respuestas de la IA? (recomendaciones de Ibrahim):**

1. **Estructura RAG (Retrieval-Augmented Generation):** "Los modelos de IA no lo saben todo; buscan información 'fresca' en bases de datos. Si tu contenido es esa base de datos bien estructurada, la IA te usará."
2. **Citas y Autoridad:** "La IA prefiere fuentes que otros sitios mencionan." Aquí el **Link Building** (visto con Daniel Quintero) "cobra una importancia vital para la credibilidad".
3. **Claridad Semántica:** "Evita ambigüedades. Usa lenguaje técnico preciso y estructurado (H1, H2, H3) para que el modelo no se confunda."

## Plantillas, criterios y umbrales exactos

El único umbral numérico explícito que da el curso:

- **Primer párrafo / respuesta directa:** "asegúrate de que el primer párrafo responda directamente a '¿Qué es [Tu Servicio]?' **en menos de 40 palabras**." (Semana 14, action item.)

Criterios (sin números, pero accionables):

- **Auditoría Final de Control de Ibrahim** (Semana 16) — tres puntos de chequeo:
  - **Contenido:** ¿Está actualizado? ¿Es único?
  - **Estructura:** ¿Hay contenido duplicado? ¿Están bien jerarquizados los encabezados?
  - **SEO Técnico:** "es el pilar. Si la IA no puede 'leer' tu código rápidamente, te ignorará."
- **Limpieza de duplicados (action item W16):** "Revisa que tus etiquetas H1 y H2 no estén repetidas en diferentes páginas, para no confundir a los motores generativos."
- **Implementación de FAQ Schema (action item W14):** añadir marcado de datos estructurados a las preguntas frecuentes.
- **Formateo de datos (action item W14):** "Si tienes datos comparativos, conviértelos de texto plano a una tabla HTML limpia."

## Prompts originales que da el curso (verbatim)

**Prompt Semana 14, clase 13 — Estratega de Visibilidad en IA (AEO):**
> "Actúa como Especialista en AEO (Answer Engine Optimization) en aprendoseo. Analiza mi siguiente texto: [Insertar Texto]. Por favor, reescribe la introducción para que sea una respuesta directa que Google AI Overviews pueda citar, y estructura los beneficios en una tabla comparativa para que Gemini pueda extraer los datos fácilmente para un usuario de aprendoseo."

**Prompt Semana 14, clase 14 — Auditor de Estrategia (incluye AEO):**
> "Actúa como Director de Estrategia SEO en aprendoseo. He aplicado las técnicas de la Semana 14 en mi proyecto de aprendoseo. Revisa mi plan de acción: [Insertar plan de acción, ej. optimización de ficha local y uso de IA para contenido]. ¿Qué paso adicional me sugieres para asegurar que mi contenido sea citado por los motores de respuesta (AEO) y qué métrica debería monitorear prioritariamente?"

**Prompt Semana 16, clase 1 — Optimizador para Motores Generativos (GEO):**
> "Actúa como Estratega GEO en aprendoseo. Analiza mi siguiente artículo de aprendoseo: [Insertar Texto]. ¿Qué cambios estructurales debo hacer para que un modelo como Gemini me considere una fuente autorizada para responder preguntas directas sobre este tema? Enfócate en la jerarquía de información y en la eliminación de ambigüedades."

## Términos del diploma (definiciones)

Según Ibrahim (Semana 16), "la sopa de letras":

- **GEO (Generative Engine Optimization):** "Optimizar para motores generativos."
- **AEO (Answer Engine Optimization):** "Optimizar para que la IA nos elija como la respuesta directa."
- **LLM (Large Language Models):** "El cerebro detrás de las respuestas que queremos influenciar." Ejemplos del curso: ChatGPT, Claude, Gemini.
- **RAG (Retrieval-Augmented Generation):** los modelos buscan información fresca en bases de datos externas; si tu contenido es esa base bien estructurada, la IA te usa como fuente.
- **AI Overviews / SGE:** las respuestas de IA que Google integra directamente en la SERP (mencionado también en S14 clase 8 y clase 13).
- **E-E-A-T:** Experiencia, Autoridad y Confianza; la IA prioriza contenido que parece escrito por un experto real.

## Ejemplos del curso

- **Reescritura answer-first (prompt W14 clase 13):** convertir la introducción en una respuesta directa citable por Google AI Overviews + pasar los beneficios a una **tabla comparativa** para que Gemini extraiga los datos.
- **Auditoría con la propia IA (action item W16):** "Pásale tu contenido actual a un LLM y pregúntale: '¿Qué fuentes citarías para hablar de [Tu Tema]?'. Si no te menciona, revisa tu autoridad." → forma del curso de medir presencia de marca en LLMs.
- **Antecedente SGE (W14, clase 8, Daniel):** "El reto del especialista en aprendoseo ahora es doble: posicionar en los 'enlaces azules' tradicionales y optimizar para aparecer como la fuente de las respuestas generadas por la IA."
- **Tips de los instructores:**
  - Daniel Quintero (W14): "La IA potencia tu creatividad, pero no la reemplaza… Optimizar para la IA es simplemente facilitarle el trabajo al algoritmo para que reconozca tu excelente contenido humano."
  - Ibrahim Mogollón (W16): "No solo escribas para humanos, escribe para que la IA te entienda. El futuro del SEO… se trata de ser la fuente de información más estructurada y confiable de tu nicho."
