---
name: seo-local
description: "Usa esta skill cuando el negocio tenga ubicación física o atienda a clientes de una zona, o cuando el sitio ofrezca servicios profesionales o marca personal, aunque el usuario no diga \"SEO local\", p.ej. \"quiero salir en el mapa de Google\", \"mi barbería/consultorio/restaurante no aparece cuando buscan cerca de mí\", \"optimiza mi ficha de Google\", \"cómo consigo reseñas\", \"mi negocio tiene dos sedes\", \"una página por cada servicio\", \"cómo sé de dónde vienen mis clientes\". Sigue el método de \"De Cero a SEO\" (aprendoseo, Semana 14, \"¿Qué es el SEO Local?\" y \"SEO para servicios, marcas personales y negocios pequeños\"): Google Business Profile, los 3 pilares (proximidad, relevancia, prominencia), NAP consistente, reseñas, una página por servicio y por zona, y medición con formulario. Entrega ficha optimizada, auditoría NAP, plan de reseñas y schema local."
compatibility: Script opcional requiere Python 3 solo con stdlib (verificar_nap.py, rastreo en vivo con User-Agent de navegador). Funciona 100% manual sin él.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/local-seo.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `local-seo.json`.

# SEO Local y SEO de servicios (S14)

Actúa como **Consultor de SEO Local en aprendoseo**. Objetivo: que cuando alguien busque un servicio "cerca de mí" o en una ciudad, el negocio aparezca en el **Local Pack** (el cuadro de mapa) y que las páginas del sitio respalden esa misma palabra clave local. Frase del curso: *"las reseñas son tu moneda de cambio"*.

> **Método completo del diploma:** [`references/metodo-diploma.md`](references/metodo-diploma.md). Esta skill **absorbe** la lección "SEO para servicios, marcas personales y negocios pequeños" (S14 L4) porque su material es corto y se combina con SEO local; no hay skill aparte.

## Cuándo usar

- Negocio con presencia física (restaurante, barbería, ferretería, consultorio) o que atiende una zona (cerrajería, limpieza).
- Profesional o marca personal con servicios (psicólogo, abogado, coach, agencia).
- Negocio con varias sedes.
- Sitio de servicios que mezcla todo en la Home.

Antes: `investigacion-de-keywords` (keywords tipo "[servicio] en [ciudad]"). Después: `schema-jsonld` para el bloque `LocalBusiness`, `plan-seo` para las tareas. Si hay tienda online, mira también `seo-ecommerce`.

## Entradas

- URL del sitio, nombre del negocio, ciudad o zonas, servicios principales.
- Enlace de la ficha de Google Business Profile (si existe) y si el negocio es físico, de zona de servicio o mixto.
- Datos reales de contacto (nombre, dirección, teléfono). No se inventan.
- Opcional: número de reseñas y rating **reales** que el usuario lea de su ficha.

## Pasos

1. **Clasifica el negocio.** Físico (dirección visible y clientes que llegan), de zona de servicio (va al cliente, no muestra dirección) o mixto. Cambia qué se verifica: una zona de servicio no necesita mapa embebido ni dirección pública.
2. **Reclama o crea la ficha de Google Business Profile.** Es la herramienta reina: alimenta el buscador, Google Maps y Waze. Si existe pero no es tuya, inicia el proceso de reclamo. La verificación depende de lo que pida Google (práctica de coaches).
3. **Optimiza la ficha para los 3 pilares.** Proximidad (cercanía, no la controlas), **relevancia** (categoría principal y secundarias correctas, descripción con servicios y ubicación, hasta 750 caracteres) y **prominencia** (fotos de calidad y reseñas). Prompt del curso en `references/metodo-diploma.md`.
4. **Audita el NAP.** Nombre, Dirección y Teléfono idénticos en la web, redes sociales y Google Maps. Con `scripts/verificar_nap.py` comparas el NAP visible con el del JSON-LD de la web. Cada ubicación es una entidad independiente.
5. **Plan de reseñas.** Un código QR en el local o un mensaje posventa para pedir la reseña (con foto, si se puede), y **responder todas**. Una ficha activa indica que el negocio sigue vivo. No ofrezcas descuentos a cambio de reseñas positivas ni filtres a quién se la pides (política de Google).
6. **Una página por servicio (y por zona).** Regla de oro del curso: *una página diferente para cada servicio*, no todo en la Home. Para zonas, páginas tipo "[servicio] en [barrio o ciudad]" con contenido propio. Toda la web debe apuntar a la keyword local, no solo la ficha (práctica de coaches).
7. **Keywords de intención local.** "[Servicio] en [ciudad]", "[servicio] cerca de mí", con barrio si aplica. Valida volumen con datos reales; si no hay, `pendiente de dato`.
8. **Medición y atribución.** Formulario de contacto específico, campo "¿Cómo nos conociste?", y preguntar al cliente cómo llegó. Si dicen "en Google" o "en el mapa", la estrategia funciona. Sin datos, no inventes conversiones.
9. **Schema local.** Genera `LocalBusiness` (o su subtipo) con `schema-jsonld`, usando solo datos que existan en la página. Con varias sedes, un bloque por ubicación.
10. **Registra tareas.** Pasa los hallazgos a `plan-seo` con verbo, prioridad y fecha.

## Salida

```
SEO LOCAL: [negocio] · Tipo: [físico | zona de servicio | mixto] · Ciudad(es): ...
1. FICHA GBP: categoría principal / secundarias / descripción (conteo de caracteres) / fotos / horario
2. AUDITORÍA NAP: tabla web vs schema vs ficha (coincide | difiere) + correcciones
3. RESEÑAS: cantidad y rating reales (o `pendiente de dato`), plan de solicitud, plantilla de respuesta
4. PÁGINAS: una por servicio y por zona, con keyword local, H1 y enlazado
5. MEDICIÓN: formulario con "¿Cómo nos conociste?", fuente de verdad
6. SCHEMA: LocalBusiness listo para pegar (si los datos son reales)
7. TAREAS: lista con verbo y prioridad (para plan-seo)
```

## Script opcional

`scripts/verificar_nap.py <url>` descarga la página (User-Agent de navegador, respeta robots.txt, un solo fetch), extrae teléfonos, enlaces `tel:`, el JSON-LD `LocalBusiness` y direcciones, y señala diferencias entre texto visible y schema. Salida JSON. Si el sitio responde 403/WAF avisa y pasa a modo manual. Escribe `local-seo.json` en `.seo-audit/<sitio>/data/` con `--sitio`.

```bash
python3 scripts/verificar_nap.py --help
python3 scripts/verificar_nap.py https://ejemplo.com/contacto --sitio ejemplo.com
```

## Reglas

- NAP idéntico en todas partes: una coma o un prefijo distinto cuenta como diferencia a corregir.
- Las categorías y la descripción de la ficha describen lo que el negocio hace, no keywords apiladas.
- Páginas por zona con contenido propio: si cambiando el nombre de la ciudad el texto sigue sirviendo igual, es una página duplicada. No las crees en masa.
- Nada de reseñas falsas ni comprometidas. Nada de dirección falsa para posicionarse en otra ciudad.
- No inventes rating, número de reseñas, posición en el mapa ni tráfico.

## Complementos opcionales (claude-seo)

Después del método del diploma, [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md) añade una rúbrica de puntaje por dimensiones, umbrales de calidad de páginas de ubicación, subtipos de schema por industria y el uso opcional de datos de pago para Maps. Es opcional y no sustituye al método.

## Gotchas

- Optimizar solo la ficha no basta: la web entera debe respaldar la keyword local.
- Reseñas de una sede no se transfieren a otra.
- Una zona de servicio no debe mostrar una dirección que no sea real.
- En servicios, la conversión es agendar, llamar o llenar un formulario: mide eso, no solo visitas.
- Un negocio de salud o legal (YMYL) exige cuidado extra en las afirmaciones; estudia el sector antes de prometer.
