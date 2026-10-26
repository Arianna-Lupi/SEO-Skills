# Complementos: SEO Local

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.** Origen: `skills/seo-local/SKILL.md`, `skills/seo/references/local-schema-types.md`, `skills/seo-maps/SKILL.md` de agricidaniel/claude-seo. Adaptado y resumido. Las cifras de estudios de terceros (Whitespark, BrightLocal, Sterling Sky) son de esa fuente y envejecen: verifícalas antes de citarlas a un cliente. Si algo contradice al diplomado, gana el diplomado.

## 1. Rúbrica de puntaje local (0 a 100)

Útil para reportar un antes y un después. Cada dimensión se evalúa Completa / Parcial / Baja solo con evidencia observada.

| Dimensión | Peso | Qué mira |
|---|---|---|
| Señales de ficha (GBP) | 25% | Categoría principal correcta, categorías secundarias, fotos, horario visible, Q&A |
| Reseñas y reputación | 20% | Cantidad, rating, recencia, respuestas del dueño, plataformas |
| On-page local | 20% | Ciudad en título y H1, NAP visible, una página por servicio, enlace `tel:` |
| NAP y citaciones | 15% | Coincidencia web, schema y ficha; directorios principales |
| Schema local | 10% | `LocalBusiness` con subtipo correcto y propiedades recomendadas |
| Autoridad local | 10% | Menciones y enlaces locales (cámara de comercio, prensa, comunidad) |

Los pesos son de claude-seo, no del curso. Úsalos como guía, no como verdad.

## 2. Casos que cambian qué revisar

- **Zona de servicio (SAB):** omite mapa embebido y dirección pública. `areaServed` con ciudades nombradas.
- **Mixto:** ambas lógicas.
- **Varias sedes:** URL rastreable por sede (`/sedes/ciudad/`), `LocalBusiness` con `@id` propio por sede y `branchOf` hacia la `Organization`.

## 3. Calidad de páginas por ubicación

- **Prueba del intercambio:** si cambiando el nombre de la ciudad el texto sigue funcionando igual, es una página puerta de entrada (doorway). Reescribe con contenido propio: barrios, equipo local, testimonios de la zona, preguntas frecuentes locales.
- Referencia del sector: más de 60% de contenido único; aviso al llegar a 30 páginas de ubicación y revisión justificada a partir de 50. No hay umbral confirmado por Google.
- Enlazado: cada página crítica a máximo 3 clics de la Home (coincide con la regla de 3 clics del diplomado).

## 4. Reseñas, con criterio

- La frecuencia importa más que el total: una racha larga sin reseñas nuevas perjudica.
- Revisión ante cualquier intento de "filtrar" quién reseña: Google lo prohíbe como interacción falsa. Salud y legal tienen límites de privacidad al responder.

## 5. Schema local

Usa el subtipo más específico (`Restaurant`, `Dentist`, `LegalService`, `Locksmith`, `HVACBusiness`, `RealEstateAgent`). Propiedades recomendadas: `name`, `address` (PostalAddress), `telephone`, `url`, `openingHoursSpecification`, `geo` (coordenadas con 5 decimales), `image`, `priceRange`, `aggregateRating` solo si las reseñas son visibles en la página. `Attorney` está obsoleto: usa `LegalService` más `Person`. El schema no es factor de ranking directo; ayuda a las rich results y a la comprensión de entidades. Genera el bloque con `schema-jsonld`.

## 6. Otras fuentes de ficha

Bing Places (alimenta Copilot y otros asistentes), listados de Apple y agregadores de datos. Reclamarlos es barato y ayuda a la consistencia del NAP; el diplomado solo menciona Apple Maps vía Yelp.

## 7. Búsqueda con IA y negocio local

Los asistentes de IA citan menciones de terceros (reseñas, directorios, listas "los mejores de"). Para el análisis completo usa `optimizacion-geo-aeo`.

## 8. Maps con datos de pago (opcional)

claude-seo incluye `seo-maps` (rastreo en cuadrícula geográfica, auditoría de ficha, inteligencia de reseñas, radio de competidores) apoyado en DataForSEO. Es de pago, requiere clave y envía datos a un tercero: solo con permiso explícito del usuario. Sin eso, la revisión manual de Local Pack (buscar la keyword desde la ciudad del cliente, modo incógnito) cubre lo esencial.

## Ideas descartadas

- Estadísticas de conversión de IA local, por no poder verificarse aquí.
- Puntajes de "Domain Authority" local, por ser métrica de terceros.
