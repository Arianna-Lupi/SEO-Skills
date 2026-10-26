# Complementos de claude-seo para imágenes

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.**
> Fuente: `skills/seo-images/SKILL.md` y `agents/seo-image-gen.md` del repo AgriciDaniel/claude-seo (licencia MIT). Adaptado. Si algo contradice el diplomado, gana el diplomado: el umbral oficial del curso es **100 kb** por imagen.

## 1. Umbrales de peso por tipo de imagen (más finos que el de 100 kb)

| Tipo | Objetivo | Aviso | Crítico |
|---|---|---|---|
| Miniaturas | menos de 50 kb | más de 100 kb | más de 200 kb |
| Imágenes de contenido | menos de 100 kb | más de 200 kb | más de 500 kb |
| Hero o banner | menos de 200 kb | más de 300 kb | más de 700 kb |

Úsalos solo para desempatar prioridades. Si el cliente trabaja con el umbral del curso, mantén 100 kb.

## 2. Formatos

- **WebP:** recomendación por defecto (soporte aproximado del 95% de los navegadores).
- **AVIF:** mayor compresión, codificación más lenta, soporte algo menor (aprox. 93%). Úsalo con `<picture>` y respaldo:

```html
<picture>
  <source srcset="foto.avif" type="image/avif">
  <source srcset="foto.webp" type="image/webp">
  <img src="foto.jpg" alt="Descripción" width="800" height="600" loading="lazy" decoding="async">
</picture>
```

- El soporte de cada formato cambia: verifícalo en caniuse.com antes de comprometer cifras con un cliente.
- Conversión local (nada se envía a terceros): `cwebp -q 82 entrada.jpg -o salida.webp`, o `ffmpeg` para AVIF. Squoosh (el navegador procesa el archivo) es la opción de coaches.

## 3. Imágenes responsivas

`srcset` y `sizes` entregan al móvil una imagen más pequeña que al escritorio:

```html
<img src="foto-800.jpg" srcset="foto-400.jpg 400w, foto-800.jpg 800w, foto-1200.jpg 1200w"
     sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px" alt="Descripción">
```

## 4. Carga y LCP

- `loading="lazy"` en todo lo que queda **bajo el pliegue**. **Nunca** en la imagen principal (daña el LCP).
- `fetchpriority="high"` en la imagen del LCP para adelantar su descarga.
- `decoding="async"` en las que no son del LCP.
- Algunos plugins (Perfmatters, EWWW, lazysizes) hacen lazy con JavaScript (`data-src`, clases `lazyload`): que no aparezca `loading="lazy"` no es un fallo en ese caso. El script lo distingue como `js_lazy`.
- Si Googlebot no ve una imagen cargada por interacción del usuario, no la indexa: evita el lazy que exige clic o scroll para contenido principal.

## 5. CLS (saltos de diseño)

- Declara `width` y `height` en cada `<img>` (o `aspect-ratio` en CSS) para reservar el espacio antes de que cargue.
- Umbral CLS bueno: 0,1 o menos en campo (ver `analisis-rendimiento`).

## 6. Nombres de archivo y metadatos

- Nombre descriptivo con guiones: `zapatillas-running-azules.webp`, no `IMG_1234.jpg`.
- Las imágenes para redes (Open Graph) conviene de 1200x630 px; revisa que `og:image` exista en las plantillas clave.
- Un sitemap de imágenes es opcional; para la mayoría de sitios no hace falta (ver `sitemap-y-robots`).

## 7. Qué quedó fuera

- Análisis de la SERP de imágenes con DataForSEO y la generación de imágenes con IA (`seo-image-gen`): requieren servicios de pago o de terceros y no están en el diplomado.
