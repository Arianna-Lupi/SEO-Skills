# Complementos de claude-seo para GEO / AEO

> **Complemento externo (claude-seo, MIT, agricidaniel), no es parte del método del diplomado.** Adaptado de `skills/seo-geo`, `agents/seo-geo.md` y sus referencias. Las cifras de estudios de terceros no las verificó esta skill: úsalas como pistas, nunca como dato del cliente.

## Postura de Google y cómo encaja con el diplomado

Google sostiene que optimizar para búsqueda con IA "sigue siendo SEO" y que AEO y GEO son nombres nuevos del mismo trabajo. Coincide con la práctica de Vero ("las estrategias GEO son la misma base", coaches/vero.md) y con Ibrahim (S16 L1: el SEO técnico es el pilar). El diplomado conserva las etiquetas AEO y GEO; úsalas, pero no vendas GEO como disciplina aparte ni prometas resultados.

## Rastreadores de IA y robots.txt

Ejecuta `scripts/ai_crawlers.py` (stdlib). Agrupa por función antes de decidir:

| Función | Rastreadores | Qué implica bloquear |
|---|---|---|
| Búsqueda con IA | OAI-SearchBot, PerplexityBot, Bingbot (alimenta Copilot) | No te citan en esas respuestas |
| Entrenamiento | GPTBot, ClaudeBot, anthropic-ai, CCBot, Google-Extended, Applebot-Extended, Bytespider, cohere-ai | Evitas que entrenen con tu contenido; no te quita de la búsqueda |
| Disparados por un usuario | ChatGPT-User, Google-Agent, Google-NotebookLM | robots.txt no los controla; usa controles de servidor |

Reglas:
- Google-Extended no afecta a Google Search ni a AI Overviews; esos dependen de Googlebot y de las directivas normales (`nosnippet`, `max-snippet`, `noindex`). No existe un archivo de exclusión solo para IA de Google.
- La decisión de permitir o bloquear es del negocio (por ejemplo, editores que quieren proteger contenido). Presenta el estado y las opciones, no impongas una.
- Los rastreadores de IA no ejecutan JavaScript de forma fiable: el contenido clave debe estar en el HTML servido (conecta con la auditoría técnica, S12 L2).

## llms.txt (opcional)

Archivo `/llms.txt` con un resumen del sitio y enlaces clave. Google dice que no lo necesita para Search ni para sus funciones de IA, y no hay evidencia sólida de que mueva citas en otras plataformas. Reporta si existe; no lo pongas como prioridad ni como parte del método.

## Citabilidad a nivel de pasaje

Heurísticas de terceros (no del diplomado):
- Bloques autosuficientes que se entiendan sin el resto de la página. Una guía práctica habitual es 130 a 170 palabras por pasaje, con la respuesta clave en las primeras 40 a 60 palabras de la sección. El diplomado fija el umbral de la definición inicial en **menos de 40 palabras** (S14 L13); respétalo para el primer párrafo.
- Frases con dato concreto y fuente, definiciones "X es...", tablas para comparativas, encabezados en forma de pregunta.
- Contenido reciente: revisa fecha de actualización de las páginas que quieres que citen.

## Señales de marca y menciones

Estudios de terceros sugieren que las menciones de marca en plataformas (YouTube, Reddit, Wikipedia, LinkedIn) se asocian más con las citas de IA que los backlinks. Coincide con S16 L1 ("la IA prefiere fuentes que otros sitios mencionan"). Acciones: presencia consistente de la marca y los autores (`sameAs` en Organization y Person, ver `schema-jsonld`), participación real en comunidades, no mención masiva artificial.

## Por plataforma (orientativo)

| Plataforma | Foco |
|---|---|
| Google AI Overviews y AI Mode | SEO clásico, pasajes citables, frescura y autoridad de entidad; son dos superficies de citas distintas, mídelas por separado |
| ChatGPT | Presencia de entidad y fuentes de referencia, acceso de OAI-SearchBot |
| Perplexity | Contenido citable y presencia en comunidades |
| Bing Copilot | Indexación en Bing (Bing Webmaster Tools, IndexNow) |

## Medición

Método del diplomado primero: pregúntale a un LLM "¿qué fuentes citarías sobre [tema]?" (S16 L1). Opcional de pago: Ahrefs Brand Radar. Descartado: DataForSEO (de pago, no está en el diplomado).
