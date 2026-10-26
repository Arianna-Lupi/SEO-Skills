# Complementos de claude-seo para briefs de contenido

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.** Autores: agricidaniel y puneetindersingh (autor original de `skills/seo-content-brief`). Origen: `skills/seo-content-brief/SKILL.md` y sus `references/` (`page-type-templates.md`, `keyword-density.md`, `excluded-domains.md`). Adaptado al español y a la terminología del curso. Si algo contradice al curso, gana el curso. Úsalo **después** de haber seguido los pasos del diplomado.

## 1. Estructura de brief más rica (añadir al brief del curso)
El curso pide: intención, metas, jerarquía, benchmark, enlaces internos y visuales. claude-seo añade estos bloques, útiles cuando el redactor es externo o el tema es competitivo:
- **Ficha de intención ampliada:** tipo de intención, **formato que Google premia** (guía larga, listado, tabla comparativa, landing, FAQ, video, paquete local), audiencia y su nivel de conocimiento. Encaja con "la brújula" (S8 L3).
- **Tabla de competidores:** URL, H2 principales, longitud aproximada, juicio de profundidad/formato/SEO/UX, y brecha principal. Longitud: cuéntala con una herramienta como wordcounter.net sobre el texto visible (Diana #1) y no la conviertas en objetivo.
- **Tres tipos de brecha:** **de tema** (nadie lo cubre), **de profundidad** (superficial), **de calidad** (datos viejos, sin experto, mal formateado). Prioriza las brechas con `impacto x ventaja competitiva / esfuerzo` como criterio cualitativo tuyo, no como cifra.
- **Ganancia de información:** una frase concreta de qué aporta esta pieza que ninguna del top tiene (dato propio, caso con resultado, cita de experto, marco original). "Más detalle" no cuenta.
- **PAA y entidades:** lista las preguntas People Also Ask como candidatas a H2/H3 y las entidades que deben aparecer (conecta con la Semana 11 lección 5). Marca con "FS" las secciones que apuntan a un fragmento destacado (respuesta directa de 40 a 60 palabras).
- **Guía de keyword por sección:** en cada H2 indica qué keyword (principal, secundaria o variación) va en el encabezado y si el cuerpo menciona la principal o una variación. Ejemplo: "H2 con la secundaria X; en el cuerpo, la principal una vez".
- **Requisitos E-E-A-T de la pieza:** autor y bio, citas o estudios con fecha, fecha de última actualización; crítico en temas sensibles. Enlaza con la skill `calidad-de-contenido-eeat`.
- **Modo "solo esquema":** si el cliente solo pide el outline, entrega H1, URL, jerarquía y una nota de redacción por sección, y omite tabla de competidores y brechas.

## 2. Reglas de calidad del brief
- **Regla de relevancia del sitio:** cada encabezado, subtema y FAQ debe poder cumplirlo la web de verdad. No copies la estructura de un competidor que cubre servicios que tu cliente no ofrece.
- **Regla de cobertura para páginas hub o "tipos de":** el esquema nombra cada categoría o servicio real del sitio, cada uno con su enlace interno; no inventes ni omitas.
- **Filtra los no competidores** al leer la SERP: enciclopedias, redes sociales y foros, marketplaces, agregadores y directorios, herramientas SEO, medios y dominios .gov y .edu. Si quedan menos de 3 competidores reales, déjalo escrito en el benchmark. Excluye también URLs de utilidad (tag, author, feed, login, carrito, privacidad).
- **Lenguaje de salida:** el brief se escribe para el redactor o el dueño del negocio; no cites nombres de herramientas ni de autores de métodos como argumento.

## 3. Colocación de la keyword principal (rúbrica)
Aparece de forma natural en: meta título (cerca del inicio), H1, URL, meta descripción, primer párrafo (primeras 100 palabras) y al menos un Alt Text. **No hace falta** en cada H2/H3, en cada párrafo ni en cada anchor de enlace interno. Errores frecuentes: obsesión por la coincidencia exacta, meter la keyword en todos los H2, olvidar el Alt Text, contar sinónimos como densidad. No hay porcentaje de densidad objetivo (coincide con S11 L2: natural, sin forzar).

## 4. Plantillas por tipo de página (más allá de Blog, Landing y E-commerce)
El curso enseña tres tipos de brief. claude-seo agrega esquemas que puedes usar como punto de partida y que se validan siempre contra la SERP:
- **Página de servicio:** qué es, para quién, cómo funciona, costos o rangos, resultados, por qué elegirnos, FAQ, CTA.
- **Página de categoría:** alcance, subproductos o subservicios enlazados, para quién, proceso, FAQ, CTA.
- **Página de ubicación:** servicio + ciudad en H1, título y primer párrafo; zonas atendidas; por qué importa lo local; equipo local; reseñas locales; FAQ local; teléfono y dirección. Se relaciona con SEO Local (S14 L2) y con la práctica de Diana de landings por localidad (#61, #62, #153).
- **Caso de éxito, Acerca de, Home:** úsalos para E-E-A-T; fuera del alcance del curso.

## 5. Diferencias con el curso (gana el curso)
| Tema | claude-seo | Diplomado | Se aplica |
|---|---|---|---|
| Meta título | 50 a 60 | 50 a 60 | 50 a 60 |
| Meta descripción | 130 a 150, sin comillas, sin marca al final | 120 a 155 con CTA | 120 a 155 |
| FAQ y Schema | No agregar FAQPage para visibilidad en Google; Google retiró los resultados enriquecidos de FAQ (afirmación de claude-seo) | S10 L6 y S14 L13 recomiendan Schema y FAQ | Seguir el curso para marcado válido, sin prometer rich results; verificar la doc oficial de Google |
| Longitud | Pisos por tipo de página y objetivos por sección | Sin cifras | No fijar objetivo de palabras (Dana #159) |
