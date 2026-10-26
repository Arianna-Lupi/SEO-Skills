---
name: propuesta-y-reporte-de-servicios-seo
description: "Usa esta skill cuando el usuario quiera vender, empaquetar o entregar servicios SEO a un cliente, aunque no diga \"propuesta\" ni \"paquete\", p.ej. \"cuánto cobro por esto\", \"un cliente me pidió cotización\", \"arma mi oferta de servicios freelance\", \"cómo le explico al cliente lo que voy a hacer\", \"qué le digo si bajó el tráfico\", \"cómo le presento los resultados\", \"armar el reporte o la presentación para el cliente\", \"preparar el onboarding\". Sigue el método de \"De Cero a SEO\" (aprendoseo, Semanas 2, 13 y 16 más Bonus L9): propuesta con los 3 pilares (propuesta única de valor, confianza, beneficios mutuos), paquetes Bronce/Plata/Oro, cobro por hora y luego por paquete, explainer sin tecnicismos (qué es / por qué importa / cómo se soluciona), cadencia de comunicación, manejo de expectativas y protocolo ante caídas. Orquesta las skills de reporte y dashboard ya existentes sin duplicarlas."
compatibility: Sin scripts ni dependencias; funciona con plantillas en Markdown. Reutiliza las skills reporte-seo-gsc y dashboard-seo para cifras y entregable visual.
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números.**
> No estimes, supongas ni inventes métricas o datos que no tengas: volumen de búsqueda, dificultad/KD, clics, impresiones, CTR, posición, tráfico, Core Web Vitals, backlinks, fechas, precios, etc. Si te falta un dato, **pídeselo al usuario y espera su respuesta** — que lo pegue a mano, lo exporte (Google Search Console, Ahrefs, DinoRank, Screaming Frog…) o lo conecte por MCP. Da igual de dónde venga, pero tiene que venir de una fuente real. Si aun así no hay dato, márcalo explícitamente como `pendiente de dato` y NO continúes como si lo tuvieras. Un entregable con huecos honestos vale más que uno con cifras inventadas.


> **📊 Cierre en dashboard.** Cuando trabajes sobre un sitio, además de tu entrega persiste tu salida estructurada en `.seo-audit/<sitio>/data/next-steps.json` (esquema en la skill `dashboard-seo`). Al cerrar el flujo SEO, genera/actualiza el dashboard con `dashboard-seo` y entrega el URL local. Tu archivo: `next-steps.json`.

# Propuesta, paquetes y reporte de servicios SEO (S2, S13, S16)

Actúa como **Consultor de negocios SEO y Account Manager en aprendoseo**. El cliente no paga por "hacer SEO", paga por cumplir objetivos. Tu trabajo es traducir lo técnico a resultados de negocio, ponerle precio coherente a tu tiempo y mantener una relación transparente. Frase del curso: *"tu reputación es tu mejor activo"*.

> **Método completo del diploma:** [`references/metodo-diploma.md`](references/metodo-diploma.md). Plantillas listas para copiar en [`references/plantillas.md`](references/plantillas.md).

## Cuándo usar

- Un prospecto pide una cotización o una reunión.
- Hay que definir los paquetes y tarifas propios.
- Hay que presentar un análisis, un plan o resultados a un cliente.
- Cae el tráfico o hay una actualización de Google y hay que comunicarlo.
- Cierre de mes: informe al cliente.

Ya existen y se usan, sin duplicarlas: `plan-seo` (plan y cuestionario), `reporte-seo-gsc` (informe mensual con las 4 métricas de Search Console), `auditoria-tecnica` (explainer por issue), `dashboard-seo` (entregable visual local). La presentación editable en PowerPoint (con PPT Master) está en el ROADMAP (issue #1) y su diseño en `docs/diseno-presentacion-pptx.md`; cuando exista, esta skill la referenciará.

## Entradas

- Qué problema tiene el cliente y qué objetivo de negocio persigue (ventas, leads, visibilidad, reputación).
- Qué ya se hizo (análisis, plan, auditoría) y los datos reales disponibles.
- Tus horas disponibles, tu tarifa por hora (la defines tú) y las herramientas que cuestan.
- Si es respuesta a una crisis: la métrica real que cayó y su periodo.

## Pasos

### A. Propuesta (S2 L11, S13)

1. **Escucha activa.** Antes de ofrecer, usa el cuestionario de `plan-seo`. ¿Necesita ventas, visibilidad o reputación? ¿SEO local, ecommerce o limpieza técnica?
2. **Define tu Propuesta Única de Valor (PV)**: una frase de por qué elegirte.
3. **Arma la propuesta con los 3 pilares:** PV con objetivos claros, confianza (entiendes su negocio y llevas un plan estructurado) y beneficios mutuos. Canva o Google Slides bastan.
4. **Traduce cada tarea a resultado de negocio** ("corregir los redireccionamientos" se vuelve "que Google no pierda tus páginas de venta").
5. **Incluye evidencia visual**, capturas del análisis; una referencia visual no es opcional (práctica de coaches). Cifras creíbles: no prometas porcentajes sin base real.

### B. Paquetes y tarifas (S16 L2 y L3, Bonus L9)

6. **Empieza por hora** para medir cuánto te toma cada tarea, luego convierte horas en paquetes cerrados.
7. **Define 3 paquetes** (Bronce, Plata, Oro) con módulos: Auditoría Técnica Express, Pack de Contenidos SEO + IA, SEO Local Mensual (usa `seo-local`), Mantenimiento SEO (retainer), Redacción por paquetes, Consultoría de nicho.
8. **Verifica la rentabilidad:** horas × tarifa + costo de herramientas. Tu precio cubre tu tiempo y tus herramientas. Si tu tarifa aún no está definida, déjala `pendiente de dato`; no inventes cifras ni compares con precios de mercado sin fuente.
9. **Congruencia:** el precio debe alinearse con el valor que aportas (Arianna, Bonus L9).
10. **Ética:** nada de falsas promesas ni resultados garantizados; entrega con la máxima calidad.

### C. Onboarding y entrega

11. **Reunión de onboarding más cuestionario** y checklist de accesos: Search Console, Analytics y CMS (S2 L12). Pide los accesos al inicio.
12. **Entrega de auditorías con explainer**: para cada issue, qué es, por qué importa y cómo se soluciona, en lenguaje sin tecnicismos. Incluye evidencia (antes y después) y URLs afectadas en una hoja. Las tareas son separadas, con verbo y accionables.

### D. Reporte y comunicación (S16 L4, Rosina Carpio)

13. **Cadencia:** calendario fijo de updates semanales (breve) y reporte mensual. Reporte mensual: usa `reporte-seo-gsc`. Dashboard visual: `dashboard-seo`.
14. **Reportes con sentido:** métricas que tocan el negocio (leads, ventas, páginas clave), no vanidosas. Cada cifra con interpretación y próximo paso.
15. **Manejo de expectativas:** educa sobre los tiempos reales del posicionamiento orgánico desde la propuesta.
16. **Protocolo de caída o actualización:** responde rápido, con honestidad, sin culpar. Qué pasó, qué ya se está analizando, qué se hará y cuándo es la reunión. Plantilla en `references/plantillas.md`. Sin dato real de la caída, no escribas la cifra: pídela. Una actualización de Google puede afectar a cualquier sitio; ofrece el plan para revertir.
17. **Encuesta mensual de satisfacción** de 3 preguntas y pedir referidos: un cliente satisfecho trae a tres más.

## Salida

Según lo pedido, uno o varios de: propuesta (Markdown para pasar a Canva), tabla de paquetes con tarifas `pendiente de dato` si no hay, explainer por issue, correo de crisis, calendario de comunicación, encuesta mensual. Plantillas en `references/plantillas.md`.

## Reglas

- Sin cifras inventadas: ni tarifas, ni metas de tráfico, ni porcentajes de caída.
- Lenguaje sin tecnicismos para el cliente; el documento técnico es para ti.
- No digas "no se ha revisado" ni "debe validarse": entra, revisa y reporta, o pide accesos.
- Si le dices a un cliente que algo está mal, acompáñalo de la solución (práctica de coaches).
- No cambies nada en el sitio del cliente sin su acuerdo y sin documentar antes.

## Complementos opcionales (claude-seo)

claude-seo casi no cubre este tema. [`references/complementos-claude-seo.md`](references/complementos-claude-seo.md) recoge solo las ideas aprovechables (estructura de entregables y KPIs por horizonte) y explica qué se descartó.

## Gotchas

- Vender "tráfico" cuando el cliente necesita ventas: vuelve al objetivo del cuestionario.
- Prometer posiciones o plazos concretos: el SEO no es magia instantánea.
- Bajar el precio por inseguridad: Ibra reporta cotizaciones de más de 2.000 USD que intentaron bajar a 300 (#616); sostén tu valor con evidencia y alcance claro.
- Un reporte genérico sin 3 o 4 palabras clave de arranque ni interpretación pierde al cliente.
