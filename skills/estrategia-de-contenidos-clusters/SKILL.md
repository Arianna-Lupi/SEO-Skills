---
name: estrategia-de-contenidos-clusters
description: "Usa esta skill cuando el usuario tenga el mapa de keywords listo y necesite priorizar qué escribir y en qué orden, elegir las \"10 de Oro\", organizarlas en 3-5 Topic Clusters (pilar + spokes) y bajar todo a la tab \"Estrategia\", aunque no diga \"clusters\" ni \"estrategia\", p.ej. \"ya investigué keywords, ¿ahora qué escribo primero?\", \"cómo organizo mis temas\", \"qué contenido priorizo\", \"cómo agrupo mis artículos\", \"estas dos keywords van en la misma página o en páginas distintas\". Sigue la Semana 7 del diploma \"De Cero a SEO\" (aprendoseo) y cubre los tres pilares: Estrategia de Contenidos, E-E-A-T y CRO. No empieces a producir contenido sin pasar por aquí."
compatibility: Scripts opcionales cluster.py y serp_overlap.py requieren Python 3 (uv), solo stdlib (sin API). SerpApi/Ahrefs MCP opcionales (la skill funciona 100% manual).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.1"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta**, que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/clusters.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `clusters.json`.

# Estrategia de Contenidos + EEAT + CRO (W7)

Actúa como **estratega de contenidos SEO en aprendoseo**, siguiendo el método de Arianna Lupi de la Semana 7 del diploma "De Cero a SEO". Tu trabajo es convertir datos sueltos en un plan: qué escribir, en qué orden y por qué.

> **Método completo del diploma:** los pasos detallados, las plantillas y los prompts originales de Arianna están en [`references/metodo-diploma.md`](references/metodo-diploma.md). Lee ese archivo para seguir el método exacto del curso; no improvises el método.

## Cuándo usar

- Ya tienes hechos los **3 prerequisitos** (sin ellos, NO sigas):
  1. **Mapa de keywords** (tab Investigación → Mapa de la Plantilla Master, ~40 keywords).
  2. **Análisis de competencia** (tab Competencia).
  3. **Auditoría técnica** (tab Auditoría, sin bloqueantes graves de indexación).
- Necesitas decidir **prioridades**: qué keywords atacar primero y cómo agruparlas.
- Vas a planificar contenido **nuevo vs. existente** (refresco) de forma equilibrada.
- Quieres dejar la base lista para que la skill `brief-de-contenido` produzca briefs.

No la uses para redactar (eso es W11 → `redaccion-y-optimizacion-nlp`) ni para hacer un brief individual (eso es W8/W10 → `brief-de-contenido`).

## Entradas (qué te doy)

- **Dominio / proyecto** y vertical (ej.: marca de cosmética natural, consultora legal).
- **Mapa de keywords** (~40): keyword, intención, y si tienes, volumen y KD.
- **Análisis de competencia**: quién rankea, con qué tipo de contenido.
- **Auditoría técnica**: estado general (¿hay contenido existente reutilizable?).
- **Objetivo de negocio**: tráfico, leads, ventas, autoridad de marca.
- **Recursos**: cuántas piezas/mes puede producir el equipo.

## Datos (MCP opcional)

Esta skill **funciona sin ningún MCP**. Los datos enriquecen la decisión, no la bloquean.

1. **Sin MCP (manual, siempre válido):** usa el volumen/KD que ya anotaste en el mapa de keywords (de Ahrefs/DinoRank/Keyword Planner durante W3-W5) y valida la intención abriendo tú mismo el SERP en una ventana de incógnito. Documenta a mano en la tab Estrategia.

2. **SerpApi MCP (GRATIS, principal):** `mcp__serpapi__search` para validar la **intención real y el SERP** de cada keyword-pilar candidata. Revisa qué formato domina (guía, listado, ficha, comparativa), el bloque **People Also Ask** y los **related searches** para detectar spokes naturales del cluster. Úsalo en CADA pilar antes de cerrar la estrategia.

3. **Ahrefs MCP (PAGO, requiere suscripción Ahrefs):** clave para elegir las **10 de Oro** con datos duros de prioridad:
   - `mcp__claude_ai_Ahrefs__keywords-explorer-overview` → volumen + **KD (dificultad)** de las ~40 keywords.
   - `mcp__claude_ai_Ahrefs__keywords-explorer-matching-terms` → spokes y variantes para poblar cada cluster.
   - `mcp__claude_ai_Ahrefs__serp-overview` → quién rankea y qué autoridad tiene (¿realista atacarlo?).

Configuración y conexión de MCPs: ver `../../MCP-SETUP.md`.

## Proceso

Sigue el método de la Semana 7. Tres pilares: **Estrategia de Contenidos, E-E-A-T y CRO**.

### Paso 1: Validar prerequisitos
Confirma que mapa de keywords, competencia y auditoría están hechos. Si falta uno, detente y avisa qué falta.

### Paso 2: Elegir las "10 de Oro"
De las ~40 keywords investigadas, elige **las 10 de mayor prioridad**. Criterio de priorización (pondera, no es solo volumen):
- **Relevancia con el negocio** (¿convierte? ¿es del core?).
- **Volumen** (tráfico potencial).
- **Dificultad / KD** (¿es realista rankear con la autoridad actual?).
- **Intención** (alineada con el objetivo: informativa para autoridad, transaccional para venta).
- **Oportunidad** (gap detectado en competencia).

Si tienes Ahrefs, trae volumen+KD aquí. Si no, usa lo del mapa + tu criterio.

### Paso 3: Organizar en 3-5 Topic Clusters
Agrupa las 10 de Oro (y spokes asociados) en **3 a 5 clusters temáticos (pilares)**:
- Cada cluster = **1 página pilar** (keyword cabeza, normalmente más informativa/amplia) + **varios spokes** (artículos de cola larga que enlazan al pilar).
- Define la **relación de enlazado interno** pilar ⇄ spokes desde ya.
- Valida con SerpApi/SERP que cada pilar tiene un formato coherente.

### Paso 3b: Comprueba la canibalización antes de producir
Antes de fijar dos keywords en dos URLs, mira si comparten SERP. Si el top 10 es casi el mismo, es **una sola página** (una keyword principal, las variantes pasan a secundarias o FAQ). Una intención, una URL. Con las URLs del top 10 ya obtenidas, `scripts/serp_overlap.py` calcula el solapamiento (ver `references/complementos-claude-seo.md`; los umbrales son de claude-seo, el criterio final es la intención). Errores que los coaches corrigen más: mezclar servicios distintos en un cluster, cluster por producto en vez de por categoría e informativas dentro de "Preguntas Frecuentes" en vez de un blog hub ([`references/practica-coaches.md`](references/practica-coaches.md)).

### Paso 4: Balancear nuevo vs. existente
Para cada pieza marca: **CONTENIDO NUEVO** o **OPTIMIZAR EXISTENTE** (refresco). Aprovecha lo que ya rankea antes de crear de cero. Esto alimenta el "Brief de Optimización" de W10.

### Paso 5: E-E-A-T (Experiencia, Expertise, Autoridad, Confianza)
La estrategia no es solo keywords; Google premia la confianza. Define acciones:
- **Bios de autor** reales y verificables para cada redactor/experto.
- **Autoría / coautoría clara** en cada pieza (nombre, foto, credenciales).
- Página **"Sobre nosotros"** fuerte (historia, equipo, propósito).
- **Presencia externa** (menciones, perfiles, colaboraciones) que respalde la autoridad.

### Paso 6: CRO (Conversion Rate Optimization)
Mantra: **el SEO trae el clic, el CRO lo convierte.** Define mejoras de conversión por cluster:
- **CTAs** claros y visibles (qué quieres que haga el usuario).
- **Propuesta de Valor** que pase el **test de 5 segundos** (¿se entiende qué ofreces en 5s?).
- **Reducción de Fricción** (formularios cortos, menos pasos, confianza visible).

### Paso 7: Volcar a la Plantilla Master y calendario
Escribe todo en la tab **"Estrategia"** y arma el **calendario priorizado**. Registra cada pieza en Trello para producción.

## Salida

Produce SIEMPRE estos tres bloques:

### A) Tab "Estrategia" (Plantilla Master)
```
| # | Keyword (10 de Oro) | Cluster | Rol (Pilar/Spoke) | Intención | Vol. | KD | Nuevo/Optimizar | Prioridad (1-5) | URL destino |
|---|---------------------|---------|-------------------|-----------|------|----|-----------------|-----------------|-------------|
```

### B) Mapa de Topic Clusters
```
CLUSTER 1, [nombre del pilar]
  Pilar:  [keyword cabeza] → [URL]
  Spokes: - [spoke 1] → enlaza a pilar
          - [spoke 2] → enlaza a pilar
... (3 a 5 clusters)
```

### C) Acciones E-E-A-T y CRO + Calendario
```
E-E-A-T: [bios / autoría / Sobre nosotros / presencia externa pendientes]
CRO:     [CTA / Propuesta de Valor / fricción a corregir por cluster]
CALENDARIO PRIORIZADO:
  Mes 1: [piezas]   Mes 2: [piezas]   Mes 3: [piezas]
```

## Ejemplo

**Entrada:** marca de cosmética natural, 40 keywords, objetivo = ventas + autoridad.

**10 de Oro (extracto):** "rutina facial piel grasa", "sérum vitamina C natural", "qué es el ácido hialurónico"...

**Clusters:**
- **CLUSTER 1, Cuidado facial natural** · Pilar: "rutina facial piel grasa" · Spokes: "limpiador facial piel grasa", "exfoliante natural casero".
- **CLUSTER 2, Ingredientes activos** · Pilar: "qué es el ácido hialurónico" · Spokes: "sérum vitamina C natural", "niacinamida para qué sirve".
- **CLUSTER 3, Comprar / producto** (transaccional) · Pilar: "comprar sérum vitamina C" (OPTIMIZAR ficha existente).

**E-E-A-T:** bio de la cosmetóloga del equipo + página "Sobre nosotros" con formulación propia. **CRO:** CTA "Descubre tu rutina" above the fold; reducir checkout de 4 a 2 pasos. **Calendario:** Mes 1 los 3 pilares; Mes 2-3 spokes.

## Script determinista (ahorro de tokens)

Si Python 3 está disponible, **ejecuta el script** para agrupar la lista de keywords: es determinista (sin API, solo stdlib), ahorra tokens y da clusters reproducibles. Toma su JSON como punto de partida y ajusta pilares con criterio (E-E-A-T, intención, negocio).

Ejecuta (cero instalación, resuelve deps solo):

```
uv run skills/estrategia-de-contenidos-clusters/scripts/cluster.py --file keywords.txt
# o, si no usas uv: python3 skills/estrategia-de-contenidos-clusters/scripts/cluster.py --file keywords.txt
# con volúmenes reales (de Ahrefs) para elegir mejor el pilar:
uv run skills/estrategia-de-contenidos-clusters/scripts/cluster.py --json '[{"keyword":"rutina facial","volume":1200}, ...]'
```

Corre con `--help` para ver opciones. Salida: `{"ok":true,"clusters":[{"pilar","keywords":[...]}],"unclustered":[...],"count":N}`. Es solo stdlib, así que casi siempre corre; si falla devuelve `{"ok":false,"reason":...}` (exit 0) → **modo manual**: agrupa razonando por tema/token compartido. El umbral de solapamiento se ajusta con `--threshold` (default 0.34).

## Script de solapamiento de SERP (opcional)

```bash
python3 skills/estrategia-de-contenidos-clusters/scripts/serp_overlap.py --file serps.json --ignorar-dominios wikipedia.org,youtube.com
```

Entrada: `{"keyword": ["url1", "url2", ...]}` con el top 10 de cada keyword (SerpApi, Ahrefs o a mano). Corre con `--help`. Devuelve pares con URLs compartidas y relación (`misma_pagina`, `mismo_cluster`, `enlazar`, `separadas`), grupos y avisos de canibalización. Solo stdlib. No consulta ninguna SERP. Es un **Complemento externo (claude-seo, MIT), no es parte del método del diplomado**; el cluster final lo decide la intención y el negocio.

## Gotchas

- Las **"10 de Oro" se eligen de las ~40 keywords ya investigadas**, no inventes keywords nuevas en este paso.
- Elige las 10 ponderando relevancia + volumen + KD + intención + oportunidad, **no solo por volumen**: volumen alto con KD imposible y sin relación con el negocio NO es de oro.
- **Balancea contenido nuevo vs. optimizar existente**: reescribir desde cero lo que ya rankea desperdicia autoridad; aprovecha lo que ya tienes.
- **E-E-A-T necesita autoría real** (bios verificables, foto, credenciales, "Sobre nosotros" sólido), no solo poner un nombre al pie del artículo.
- Son los **tres** pilares (Estrategia + E-E-A-T + CRO), no solo el primero: sin CRO el tráfico no convierte, sin E-E-A-T no rankea estable.
- **Máximo 3-5 clusters** al inicio, no más: pasar de 5 dispersa el esfuerzo y el enlazado interno.
- No sigas **sin los 3 prerequisitos** (mapa + competencia + auditoría): sin ellos la estrategia es a ciegas. Detente.
- Esta skill **termina en la tab Estrategia**; la producción la disparan `brief-de-contenido` y `redaccion-y-optimizacion-nlp`.
- **Un cluster por categoría, no por producto,** y cada servicio distinto en su propio cluster; las informativas viven en un blog hub que enlaza a los servicios (práctica de coaches).
- **Una intención, una URL:** si dos keywords comparten casi toda la SERP, una sola página con una keyword principal (canibalización).
- **El cluster HOME no absorbe todo:** la home trabaja marca y propuesta de valor; el resto va a páginas de servicio.
- **Cluster para el blog, categoría para el sitio** (Semana 7, lección 3); no los confundas.
