# Complementos: SEO de ecommerce

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.** Origen: `skills/seo-ecommerce/SKILL.md` y `scripts/schema_ecommerce_validate.py` de agricidaniel/claude-seo. Adaptado y resumido. Si algo contradice al diplomado, gana el diplomado.

## 1. Puntaje de la ficha de producto (0 a 100)

| Categoría | Peso | Criterio |
|---|---|---|
| Schema completo | 25% | Campos obligatorios y recomendados de `Product` |
| Título y meta | 15% | Keyword, longitud, formato |
| Imágenes | 20% | Alt, formato, tamaño, cantidad (al menos 3) |
| Contenido | 20% | Descripción única, especificaciones, reseñas |
| Enlazado interno | 10% | Migas de pan, relacionados, enlace a colección |
| Técnico | 10% | Velocidad, móvil, canónica |

Checklist adicional: título con formato `[Producto] - [Característica] | [Marca]` y menos de 60 caracteres; meta de menos de 155 caracteres con beneficio, precio o envío y llamado a la acción; descripción de al menos 200 palabras; tabla de especificaciones; imágenes de al menos 800 px.

## 2. Reglas de validación del schema `Product`

1. Obligatorios: `name`, `image`, `offers` (usa `Offer`, no `AggregateOffer`, en listados de comerciante).
2. `price` como número en texto, sin símbolo de moneda; `priceCurrency` en ISO 4217.
3. `availability` con la URL completa de schema.org (por ejemplo `https://schema.org/InStock`).
4. `image` como lista con al menos una URL de alta resolución.
5. Si hay `brand`, que `brand.name` no esté vacío ni sea "N/A".
6. `priceValidUntil` en ISO 8601.
7. Si hay `aggregateRating`, exigir `ratingValue` y `reviewCount`.
8. Recomendados: `sku`, `description`, `brand`, `gtin` o `mpn`, `review`, `shippingDetails`, `hasMerchantReturnPolicy`.

El script `auditar_producto.py` de esta skill aplica las reglas 1 a 4, 7 y la presencia de recomendados.

## 3. Brechas entre orgánico y Google Shopping

Cruzar las keywords por las que la tienda ya rankea con su presencia en Google Shopping: solo orgánico (crear feed en Merchant Center), solo Shopping (crear guías de compra y comparativas), ambos (verificar consistencia de precio y schema), ninguno (baja prioridad). Requiere datos de pago (DataForSEO) o Merchant Center; es opcional y envía consultas a un tercero, solo con permiso del usuario.

## 4. Inteligencia de precios y marketplaces

claude-seo compara precios y vendedores en Google Shopping y Amazon con DataForSEO Merchant API (de pago, con control de costos por llamada). Fuera del alcance del diplomado y de las herramientas gratuitas.

## 5. Protocolos de compra con IA

claude-seo documenta un protocolo abierto de comercio (UCP) y un verificador de perfil. El estado de adopción cambia rápido y parte de lo reportado no está confirmado en fuentes primarias. Si el cliente pregunta, remite a `optimizacion-geo-aeo` y verifica en la documentación oficial de Google Merchant antes de prometer nada.

## Ideas descartadas

- Replicar el análisis de Amazon y Shopping: pago y fuera del curso.
- Scripts de validación de UCP: tema inmaduro.
