---
name: calidad-de-contenido-eeat
description: "Usa esta skill para revisar la calidad real de una pieza de contenido (borrador o publicada) antes o después de publicar, aunque el usuario no diga \"E-E-A-T\", p.ej. \"está optimizado pero no posiciona\", \"suena a IA, revísalo\", \"este artículo tiene autor/fuentes suficientes\", \"es contenido delgado o está bien\", \"cómo lo hago más confiable\", \"que la IA lo cite\". Aplica el método del diploma \"De Cero a SEO\" (aprendoseo): los 4 pilares E-E-A-T de la Semana 7, los 3 pilares de calidad y la humanización de la Semana 11, y los riesgos de la IA y la citabilidad de la Semana 14. Entrega un informe Problema, Por qué importa, Recomendación, con prioridades."
compatibility: Scripts calidad_contenido.py y ai_tells.py requieren Python 3 (solo stdlib; --url usa urllib con User-Agent de navegador y respeta robots.txt). SerpApi MCP (gratis) opcional; funciona 100% manual con la rúbrica.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta**, que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/content-briefs.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `content-briefs.json` (campo `quality_review`).

# Calidad de contenido y E-E-A-T (Semanas 7, 11 y 14)

Actúa como **editor/a SEO senior en aprendoseo**. Esta skill revisa una pieza (borrador o publicada) y responde una pregunta: **¿esta página es una fuente fiable y útil, o parece generada sin criterio?** Se apoya en el pilar E-E-A-T de la Semana 7 (lección 5), en los 3 pilares de calidad de la Semana 11 (intención, keywords naturales y valor para el usuario) y en los riesgos de la IA de la Semana 14 (lección 12). El mantra sigue siendo **"escribe para humanos, optimiza para robots"**.

> **Método completo del diploma:** [`references/metodo-diploma.md`](references/metodo-diploma.md). Lista de revisión y severidades: [`references/rubrica-revision.md`](references/rubrica-revision.md). Criterio de los coaches: [`references/practica-coaches.md`](references/practica-coaches.md).

## Cuándo usar

- Antes de publicar: pasar una pieza por revisión editorial (después de `redaccion-y-optimizacion-nlp`).
- En una auditoría de contenido: decidir qué páginas están flojas, delgadas o sin autoría.
- Temas sensibles (salud, dinero, legal, seguridad): reforzar fuentes y credenciales.
- El cliente pregunta "¿por qué no posiciona si está optimizado?" y el problema parece de calidad, no técnico.
- Quieres que la pieza sea más "citable" por las respuestas de IA (Semana 14, lección 13).

No la uses para redactar (eso es `redaccion-y-optimizacion-nlp`), ni para el balance de una auditoría técnica (`auditoria-tecnica`). Si la pieza ya existe y hay que mejorarla con datos de Search Console, sigue con `actualizacion-de-contenido`.

## Entradas (qué te doy)

- **URL** o el **texto/HTML** de la pieza, con su **keyword** y **tipo de página** (blog, servicio, producto, ubicación, home).
- Quién la firma o debería firmarla, y qué experiencia real tiene esa persona o marca.
- Si el tema es sensible (YMYL) y qué fuentes institucionales existen.
- Opcional: brief original, para comprobar que se cumplió la intención.

## Datos (MCP opcional)

Funciona sin MCP. Para ver la SERP y comparar contra la competencia: `mcp__serpapi__search` (gratis) o lectura manual del top 3. El script revisa señales detectables en el texto o el HTML; **la valoración de autoridad externa (menciones, enlaces entrantes) requiere datos reales de Ahrefs u otra fuente**: si no los tienes, queda `pendiente de dato`.

## Proceso (pasos del diplomado)

### Paso 1. Confirma la intención (S11 L2, pilar 1)
¿La pieza responde lo que el usuario espera encontrar, en el formato que la SERP premia? Una página que no cumple la intención no se arregla con E-E-A-T.

### Paso 2. Revisa los 4 pilares E-E-A-T (S7 L5)
- **Experiencia:** ¿quien escribe tiene vivencia de primera mano? Google lo deduce por cómo escribes y si aporta valor genuino.
- **Especialización:** ¿hay conocimiento profundo demostrable?
- **Autoridad:** ¿hay trayectoria o validación externa (otros sitios te citan, contenido en otros lugares)?
- **Confiabilidad (el pilar más importante):** ¿es seguro el sitio y está claro quién está detrás de la información?

### Paso 3. Señales a comprobar en la página
- **Autoría clara:** nombre, foto, biografía con experiencia. Si no eres experto, **coautoría** con quien sí lo sea.
- **Página "Sobre nosotros" sólida** y datos de contacto visibles.
- **Presencia externa** que respalde la autoridad.
- Temas técnicos o delicados: identifica expertos que validen o cocreen.

### Paso 4. Valor real y anti relleno (S11 L2 y L6; S14 L12)
- La pieza aporta algo que la SERP no tiene (caso, dato propio, ejemplo, opinión experta). Google penaliza el contenido de relleno.
- **Humanización obligatoria** del texto de IA: historias, metáforas, opinión experta, voz de marca (checklist en la rúbrica).
- **Fact-checking:** cada dato estadístico o nombre técnico se verifica antes de publicar. La IA alucina.
- Legibilidad en móvil: párrafos de 3 a 4 líneas, negritas, listas.

### Paso 5. Contenido delgado
Una página es delgada cuando no resuelve la intención, repite lo que ya dicen todos sin aportar o es relleno. **La longitud no es el criterio:** 600 palabras que responden la intención superan a 3000 con paja (práctica de coaches). Compara contra el top 3 qué subtemas faltan.

### Paso 6. Citabilidad para respuestas de IA (S14 L13, opcional)
Primer párrafo que responde la pregunta principal de forma directa (en menos de 40 palabras), listas y tablas limpias, Alt Text en imágenes, FAQ solo si las preguntas existen en la página, y marcado Schema coherente con el texto visible. Profundiza con la skill `optimizacion-geo-aeo`.

### Paso 7. Entrega el informe con prioridades
Cada hallazgo con el método de feedback de los coaches: **Problema, Por qué importa, Recomendación** (con texto de ejemplo). Severidad: alta (afecta confianza o seguridad), media, baja.

## Opcional: complementos externos

Después del método del diplomado, [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md) añade la prueba **Quién / Cómo / Por qué** de Google, una rúbrica con pesos internos, suelos de cobertura por tipo de página y un detector de relleno de IA. Es un **Complemento externo (claude-seo, MIT), no es parte del método del diplomado**.

## Script determinista (ahorro de tokens)

```bash
python3 skills/calidad-de-contenido-eeat/scripts/calidad_contenido.py --file pagina.html --tipo blog
python3 skills/calidad-de-contenido-eeat/scripts/calidad_contenido.py --url https://ejemplo.com/post --tipo servicio
# marcas de texto genérico de IA (en la skill de redacción):
python3 skills/redaccion-y-optimizacion-nlp/scripts/ai_tells.py --file articulo.md --keyword "keyword"
```

Corre con `--help` para ver opciones. Devuelve `senales` (autoría, bio, fechas, experiencia, fuentes externas, contacto), `flags` con severidad y afirmaciones con cifra sin fuente. Con `--url` respeta robots.txt, usa un User-Agent de navegador y hace una sola petición; si hay WAF te pide guardar el HTML. Son señales detectables, **no una nota de autoridad**. Sin Python, usa la rúbrica a mano.

## Salida

```
REVISIÓN DE CALIDAD Y E-E-A-T: [URL o título] · Tipo: [..] · Keyword: [..]
Veredicto: [lista para publicar | publicar con ajustes | reescribir secciones | no publicar]
| Área | Estado (OK / Ajustar / Falla) | Problema | Por qué importa | Recomendación |
Áreas: Intención · Experiencia · Especialización · Autoridad · Confiabilidad · Autoría · Valor real/relleno · Fact-checking · Escaneabilidad · Citabilidad IA
Pendientes de dato: [autoridad externa, etc.]
Acciones (con verbo, para Trello): [..]
```

Persiste en `.seo-audit/<sitio>/data/content-briefs.json` en el campo `quality_review` del brief correspondiente.

## Ejemplo

*Ilustrativo.* Entrada: guía de "cómo cuidar un piercing" sin firma, con un porcentaje sin fuente y un H2 sobre historia del piercing.
- **Autoría (alta):** sin firma. Por qué importa: tema de salud, la confianza es el pilar principal. Recomendación: firma con bio del profesional que lo practica y revisión por un profesional sanitario.
- **Afirmación sin fuente (alta):** el porcentaje se verifica en una fuente institucional o se elimina.
- **Intención (media):** el usuario quiere saber si duele, cuánto tarda en cicatrizar y qué cuidados necesita; la historia sobra o va al final.
- **Citabilidad (baja):** abrir con una respuesta de menos de 40 palabras y pasar los cuidados a una lista.

## Gotchas

- **El E-E-A-T no se "pone", se demuestra:** un nombre al pie sin bio ni credenciales no suma.
- **No inventes credenciales, testimonios ni cifras** para mejorar la señal. Mejor dejarlo pendiente.
- **No atribuyas una cualificación que la persona no tiene** ni prometas "garantizar posiciones" ni "somos los mejores" sin evidencia.
- **Longitud no es calidad:** no recomiendes alargar para llegar a una cifra.
- **La IA propone, tú validas:** si el borrador es de IA, exige la humanización y el fact-checking.
- **Un detector de IA no es un veredicto.** Las marcas del script son pistas para editar.
- **Temas sensibles:** fuentes primarias o institucionales; la competencia sirve para ver temas, no como fuente principal.
