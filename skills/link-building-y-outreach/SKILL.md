---
name: link-building-y-outreach
description: Construye el pipeline completo de adquisición de enlaces nuevos — descubrimiento de fuentes candidatas (directorios, prensa, B2B, asociaciones), análisis de brecha vs. competencia, scoring por relevancia/autoridad/viabilidad, y tabla maestra de oportunidades con contenido de outreach listo para copiar y pegar. Usa esta skill cuando el usuario pida "consígueme backlinks", "necesito más enlaces", "qué directorios me faltan", "analiza los enlaces de mi competencia", "hazme un plan de link building/outreach". NO uses esta skill para limpiar un perfil de enlaces existente ni generar disavow (eso es `auditoria-de-backlinks-toxicos`, que conviene correr ANTES de construir enlaces nuevos).
compatibility: Funciona sin MCP (research manual de directorios/prensa/asociaciones). Ahrefs MCP opcional para el gap de competencia (`site-explorer-referring-domains`, `organic-competitors`). SerpApi MCP opcional para validar presencia en SERP de directorios.
metadata:
  author: aprendoseo
  milestone: SEO skills (link building)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes URLs, datos de contacto ni cifras de tráfico/DR de una fuente candidata.** Si no verificaste que un directorio/medio existe y acepta listados, dilo explícito y marca `pendiente de verificar` — no inventes un URL de submission que no confirmaste.

# Link Building y Outreach

Construye el pipeline de adquisición de enlaces nuevos de punta a punta: desde encontrar fuentes candidatas hasta dejar el contenido de outreach listo para copiar y pegar. Corre primero `auditoria-de-backlinks-toxicos` si el perfil de enlaces del sitio no está limpio — no tiene sentido construir sobre un perfil con spam sin revisar.

## Cuándo usar

- Sitio con perfil de enlaces limpio (o recién limpiado) que necesita crecer autoridad.
- Negocio local que aún no está en los directorios básicos (Google Business Profile, Yelp, cámaras de comercio, directorios de nicho).
- Cliente que pregunta "¿qué enlaces tiene mi competencia que yo no tengo?"
- Preparar una ronda de outreach con contenido ya redactado, no solo una lista de ideas.

## Proceso

**1. Descubrimiento de fuentes candidatas**
Busca por categoría, no al azar:
- **Directorios locales y nacionales** (Google Business Profile, Yelp, directorios del país/región, cámaras de comercio).
- **Relaciones B2B existentes** (proveedores, revendedores, clientes que ya mencionan la marca — el ask más fácil de todos).
- **Prensa y medios locales** (ángulo de historia real: caridad, evento, temporada — no un press release genérico).
- **Asociaciones industriales y patrocinios comunitarios** (autoridad alta pero casi siempre de pago — van al final de la priorización).

Para cada fuente: URL de submission, costo, y si ya existe un listado (necesita corrección) o es nuevo (necesita alta).

**2. Análisis de brecha vs. competencia**
Con Ahrefs MCP (`site-explorer-referring-domains` de 2-3 competidores directos) o export manual: identifica qué dominios enlazan a la competencia pero no al cliente. Filtra solo por relevancia genuina (temática o geográfica) — un dominio que enlaza a la competencia por azar no es una oportunidad real.

**3. Scoring y priorización**
Puntúa cada oportunidad en 3 ejes — ver [`references/metodologia-scoring.md`](references/metodologia-scoring.md):
- **Relevancia**: qué tan ligada está la fuente al rubro/geografía del cliente.
- **Autoridad**: qué tan confiable/establecida es la fuente.
- **Viabilidad**: qué tan fácil y barato es conseguir el enlace (peso más alto para el tier Alto).

Clasifica en 3 tiers (Alto/Medio/Bajo) y etiqueta el tipo de adquisición: `earned` (por relevancia/relación/listado gratis) vs. `sponsored-disclosed` (membresía o patrocinio pago, siempre declarado — nunca esquema de enlace pago oculto).

**4. Tabla maestra + contenido de outreach**
Una fila por oportunidad: `source, opportunity_type, url, contact_status, priority, notes`. Para el tier Alto, redacta el contenido listo para copiar y pegar (texto de submission a directorio, borrador de email a prensa/B2B) — no dejes solo el nombre de la fuente, deja el trabajo hecho.

## Salida

- **Pool de fuentes candidatas** por categoría con costo y estado (existente/nuevo).
- **Tabla de brecha vs. competencia** con las oportunidades genuinamente relevantes.
- **Tabla maestra con scoring** (relevancia/autoridad/viabilidad) y tier de prioridad.
- **Contenido de outreach round 1** listo para usar en las oportunidades de tier Alto.

## Gotchas

- **Viabilidad pesa más que autoridad en el tier Alto.** Una fuente barata y fácil con relevancia real gana a una fuente prestigiosa que cuesta dinero o meses de ida y vuelta editorial — esas van a tier Bajo aunque el nombre suene mejor.
- **Corregir un listado existente es más fácil que crear uno nuevo** — antes de buscar fuentes nuevas, revisa si el cliente ya tiene presencia con datos desactualizados (dirección, NAP) en los directorios básicos. Si el NAP no está confirmado, corre `investigacion-de-keywords`/auditoría de NAP antes.
- **"Earned" vs. "sponsored-disclosed", nunca esquema de enlace pago oculto.** Cualquier oportunidad que implique pago se declara como tal en la nota — no se presenta como si fuera orgánica.
- **Un gap de competencia sin filtro de relevancia es ruido.** Un directorio genérico sin relación temática ni geográfica no es una oportunidad real solo porque la competencia esté ahí.
- **No inventes URL de submission ni email de contacto** de una fuente que no verificaste — marca pendiente de verificar y seguí.
- **Esta skill construye, no limpia.** Si el perfil de enlaces del sitio tiene spam/toxicidad sin revisar, corre primero `auditoria-de-backlinks-toxicos`.
