# Complementos de claude-seo para schema

> **Complemento externo (claude-seo, MIT, agricidaniel), no es parte del método del diplomado.** Adaptado al español. Estado verificado el 26 de octubre de 2026 contra la documentación de Google (FAQPage) y la tabla `skills/seo-schema/references/deprecated-types-2024-2026.md` de claude-seo.

## Estado de los tipos (para decidir qué recomendar)

**Activos, recomienda con libertad:** Organization, LocalBusiness, Product (+Offer, ProductGroup), Service, Article, BlogPosting, NewsArticle, Review, AggregateRating, BreadcrumbList, WebSite, WebPage, Person, ProfilePage, ContactPage, VideoObject, ImageObject, Event, JobPosting, Course, DiscussionForumPosting, QAPage, SoftwareApplication.

**Sin rich result en Google (no los vendas como "estrellas" o "desplegable"):**

| Tipo | Estado | Qué hacer |
|---|---|---|
| FAQPage | Rich result retirado el 7 de mayo de 2026 (antes, desde agosto de 2023, solo sitios de gobierno y salud) | El diplomado lo enseña para IA (S14 L13). Mantén el marcado si las preguntas son visibles; no prometas SERP. Para Q&A real de usuarios usa QAPage. |
| HowTo | Retirado en septiembre de 2023 | Estructura los pasos con H2/H3 y listas; el schema no aporta en Google. |
| SpecialAnnouncement | Deprecado el 31 de julio de 2025 | Event o Article. |
| ClaimReview, VehicleListing, EstimatedSalary, LearningVideo | Retirados en junio de 2025 | Product, JobPosting con baseSalary, VideoObject según el caso. |
| Course Info (carrusel) | Retirado en junio de 2025 | La tarjeta Course sigue activa. |
| Practice Problem | Soporte retirado en enero de 2026 | No recomendar. |
| Dataset | Vigente solo para Dataset Search | No aconsejar quitarlo. |

Los tipos retirados pueden seguir siendo vocabulario válido de schema.org; lo que cambia es que Google ya no los muestra.

## Reglas extra

- **JSON-LD sale en el HTML inicial** (renderizado en servidor) para Product y Offer; el marcado inyectado por JavaScript puede procesarse con retraso.
- **Solo marcas lo que existe en la página.** Ratings, precios, FAQs y pasos deben verse. Es la misma regla que enseña Ari.
- URLs absolutas, fechas ISO 8601, sin texto de relleno entre corchetes.
- Para Product: confirma `name`, `image` y `offers` (mínimo para listados de comerciante), `offers` de tipo Offer, y política de devoluciones y envío si aplican.

## Validación automática

`scripts/validate_schema.py` (stdlib) lee una URL, un HTML o un JSON y reporta: falta de `@context`, requeridas ausentes, placeholders, URLs relativas, fechas inválidas, ratings incompletos y tipos retirados. Es una revisión estática: el Rich Results Test sigue siendo la validación final.

```bash
python3 scripts/validate_schema.py --url https://sitio.com/pagina --out .seo-audit/sitio.com/data/schema-validation.json
```

## Descartado

- Los generadores de schema de comercio avanzado (reservas, pedidos, ProfilePage) de `schema_generate.py`: el diplomado no los cubre.
