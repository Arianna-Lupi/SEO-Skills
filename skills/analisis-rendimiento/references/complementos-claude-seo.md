# Complementos de claude-seo para el análisis de rendimiento

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.**
> Fuente: `skills/seo-technical/SKILL.md` (sección Core Web Vitals) y `scripts/pagespeed_check.py`, `scripts/crux_history.py` del repo AgriciDaniel/claude-seo. Adaptado. Si algo contradice el diplomado, gana el diplomado.

## Umbrales vigentes de Core Web Vitals

Google evalúa el **percentil 75** de usuarios reales (campo). Una URL "aprueba" si las tres métricas están en "bueno".

| Métrica | Bueno | Necesita mejora | Malo | Qué mide |
|---|---|---|---|---|
| LCP | hasta 2,5 s | 2,5 a 4 s | más de 4 s | Carga del elemento principal |
| INP | hasta 200 ms | 200 a 500 ms | más de 500 ms | Respuesta a toda interacción de la visita |
| CLS | hasta 0,1 | 0,1 a 0,25 | más de 0,25 | Estabilidad visual |

- **INP sustituyó a FID en marzo de 2024.** Ya no se reporta FID. INP es un dato de **campo**: Lighthouse no lo mide; usa **TBT** como proxy de laboratorio.
- Los rangos "necesita mejora" y "malo" salen de la documentación pública de web.dev: verifícalos ahí si el informe es formal.

## Cómo obtener datos de campo sin instalar nada

1. **Search Console > Core Web Vitals** (gratis, es la fuente del veredicto de Google; agrupa URLs similares, lo que encaja con auditar por plantillas).
2. **PageSpeed Insights**: la sección "Descubre lo que tus usuarios reales están experimentando" es CrUX. Si no aparece, la URL no tiene tráfico suficiente: anótalo como `pendiente de dato`, no lo rellenes con laboratorio.
3. `scripts/psi_campo.py URL1 URL2 --confirmo`: hace esa consulta por la API pública de Google y entrega LCP, INP y CLS de campo con veredicto. **Envía las URLs a Google: pide permiso al usuario.** Clave opcional en `PSI_API_KEY`.

## Diagnóstico por métrica (guía de causas probables)

| Métrica en rojo | Causas habituales | Primer paso |
|---|---|---|
| LCP | Imagen hero pesada o con `loading="lazy"`; servidor lento; CSS/JS que bloquea el render | Comprimir/convertir el hero, quitar lazy del hero, `fetchpriority="high"` |
| INP | JavaScript pesado en el hilo principal; scripts de terceros; manejadores lentos | Diferir o quitar scripts no críticos; revisar TBT en Lighthouse |
| CLS | Imágenes sin `width`/`height`; fuentes sin `font-display`; anuncios o embeds sin espacio reservado | Reservar espacio y declarar dimensiones |

Subpartes del LCP (retraso de carga, descarga y render del recurso) ayudan a decidir si el cuello es el servidor o la imagen: se ven en la pestaña "Performance" de DevTools. Es optativo.

## Otros límites útiles

- Googlebot lee los primeros **2 MB de HTML**: si el HTML pesa más por base64 o JS en línea, hay contenido que no se indexa.
- La experiencia móvil manda: Google indexa mobile-first, corre siempre `--mobile`.
