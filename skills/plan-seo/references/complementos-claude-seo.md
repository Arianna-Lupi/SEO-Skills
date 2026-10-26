# Complementos: Plan SEO

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.** Origen: `skills/seo-plan/SKILL.md` y `skills/seo-plan/assets/*.md` de agricidaniel/claude-seo. Adaptado. Si algo contradice al diplomado, gana el diplomado.

## 1. Fases por semanas (alternativa al plan por meses)

Para proyectos más largos, claude-seo propone 4 fases: **Fundación** (semanas 1 a 4: técnica, páginas núcleo, schema esencial, analítica), **Expansión** (semanas 5 a 12: contenido de páginas principales, blog, enlazado interno, SEO local si aplica), **Escala** (semanas 13 a 24: contenido avanzado, link building, GEO, rendimiento) y **Autoridad** (meses 7 a 12: contenido de liderazgo, PR, schema avanzado). Equivale a estirar los Meses 1 a 4 del diplomado.

## 2. Entregables sugeridos

Estrategia, análisis de competidores, calendario de contenido, hoja de ruta de implementación y estructura del sitio. En el repo se cubren con: Plantilla Master (estrategia y calendario), `analisis-serp-y-competencia`, `arquitectura-y-enlazado-interno` y este plan.

## 3. Tabla de KPI con horizontes

| Métrica | Base | 3 meses | 6 meses | 12 meses |
|---|---|---|---|---|
| Tráfico orgánico | real | meta | meta | meta |
| Rankings de keywords | real | meta | meta | meta |
| Páginas indexadas | real | meta | meta | meta |
| Core Web Vitals | real | meta | meta | meta |

Rellena solo con base real. claude-seo incluye "Domain Authority"; es métrica de terceros, úsala solo como referencia.

## 4. Plantillas por tipo de negocio

SaaS, servicio local, ecommerce, editorial, agencia y genérica. En este repo: ecommerce y local tienen su skill propia (`seo-ecommerce`, `seo-local`). Idea descartada: replicar las plantillas SaaS y editorial, porque el diplomado clasifica proyectos en E-commerce, Servicios y Contenido.

## 5. Puerta de calidad para páginas por ubicación

Aviso a partir de 30 páginas de ubicación y parada dura a partir de 50 (exigir justificación). Ver `seo-local` para el criterio de contenido único.

## 6. Datos de pago opcionales

DataForSEO (competidores, volumen, dificultad). Opcional y de pago; el diplomado trabaja con herramientas gratuitas o las del alumno.

## 7. Archivos de salida del plan (idea, no adoptada tal cual)

claude-seo entrega `SEO-STRATEGY.md`, `COMPETITOR-ANALYSIS.md`, `CONTENT-CALENDAR.md`, `IMPLEMENTATION-ROADMAP.md` y `SITE-STRUCTURE.md`. En este repositorio esos documentos se reemplazan por la Plantilla Master y los briefs del diplomado (`generar_master.py` y `generar_briefs.py`), que son el formato que entrega la comunidad. De claude-seo solo se aprovechó la idea de un calendario con prioridades y dependencias.
