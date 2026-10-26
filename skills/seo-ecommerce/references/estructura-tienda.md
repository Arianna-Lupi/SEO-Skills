# Estructura de tienda: colecciones, variantes, paginación y filtros

> Origen: práctica de coaches con Shopify (perfil de Juan, SEO técnico) y de Ibra/Ari. **El diplomado no desarrolla estos puntos técnicos**; solo establece que las colecciones y los productos son las páginas críticas. Donde claude-seo o Google recomiendan algo distinto, se deja anotado para decidir con el cliente.

## Colecciones

- Jerarquía padre e hijas; una categoría padre debería tener al menos dos hijas.
- Muchas colecciones al mismo nivel diluyen la importancia y el crawl budget. No hay cantidad ideal: **cada colección debe apuntar a una keyword útil**.
- Productos por marca (colección de marca) cuando la marca se busca.
- Cada colección lleva H1 con la keyword, descripción propia, migas de pan y metaetiquetas.
- Nombres estables (evergreen). Una colección temporal se redirige al terminar, no se borra sin redirección.

## Canónicas

- En Shopify las canónicas no vienen bien por defecto: añade `<link rel="canonical" href="{{ canonical_url }}" />` antes de `</head>` en el código del tema.
- Si el producto no tiene variantes, el producto original es su propia variante. Una URL de variante con canónica a la URL sin variante no suele ser un problema.
- Un producto con varias URLs (dentro de colecciones, `/collections/x/products/y`) debe apuntar a una sola URL canónica.

## Variantes

- Talla, color y similares viven dentro de un mismo producto; no crees un producto por variante salvo que la variante tenga demanda de búsqueda propia (por ejemplo un color con keyword propia).
- El schema `Product` describe el producto; si hay variantes con distinto precio, usa los precios reales.

## Paginación

- Criterio de la práctica de coaches (Juan): las URL paginadas no deben indexarse; canónica a la URL principal de la paginación y noindex.
- **Discrepancia con otras fuentes:** Google y claude-seo recomiendan canónica autorreferenciada en cada página paginada y no combinar canónica a la página 1 con noindex, porque son señales contradictorias. Decide con el cliente y documenta la elección. Lo que sí se mantiene: que los productos sean alcanzables por enlaces rastreables.

## Filtros y parámetros

- Parámetros de filtros o de vendors: mejor como colecciones propias cuando tienen demanda (por ejemplo "zapatillas rojas"), y bloqueados o noindex cuando no.
- No abras todas las combinaciones de filtros al rastreo.

## Fichas de producto

Ver el checklist en `SKILL.md` paso 4. Cada ficha tiene H1 único con el nombre del producto, FAQ, reseñas visibles, alt en imágenes, breadcrumb y producto relacionado.

## Qué no es posible en Shopify

Editar el sitemap (se genera solo), subir WebP o AVIF, borrar la colección "all". Ver `plan-seo` para diferir al developer lo que no se pueda.
