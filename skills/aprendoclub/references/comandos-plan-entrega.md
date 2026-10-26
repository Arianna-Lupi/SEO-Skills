# Comandos de verticales, plan y entrega

## `/aprendoclub local`

- **Ejecuta:** `seo-local` (Semana 14): ficha de Google Business Profile, proximidad, relevancia y prominencia, NAP consistente (`verificar_nap.py`), reseñas, una página por servicio. También sirve para servicios y marca personal.
- **Pide:** URL de contacto y los datos de la ficha (nombre, dirección, teléfono) tal como están en Google.
- **Ejemplo:** `/aprendoclub local`
- **Salidas:** `local-seo.json`.

## `/aprendoclub ecommerce <sitio>`

- **Ejecuta:** `seo-ecommerce` (Semana 14): colecciones, fichas de producto (`auditar_producto.py`), schema `Product`, canónicas y paginación.
- **Nota:** la regla de paginación de Juan (canónica a la página 1 más noindex) difiere de la recomendación de Google; la skill lo documenta para decidirlo con el cliente.
- **Ejemplo:** `/aprendoclub ecommerce mitienda.com`
- **Salidas:** `ecommerce.json`.

## `/aprendoclub plan <sitio>`

- **Ejecuta:** `plan-seo` (Semanas 2 y 13): objetivos SMART, plan por meses, Plantilla Master y briefs. Si además hay que entregar propuesta y reporte al cliente, usa `agente-plan-y-entrega`.
- **Ejemplo:** `/aprendoclub plan midominio.com`
- **Salidas:** `next-steps.json`, `plan-seo.json`, archivos en `.seo-audit/<sitio>/entregables/`.

## `/aprendoclub project`

- **Ejecuta:** `proyeccion-seo-gsc`: escenarios "si se cumple el plan" a partir de un export de Search Console, y seguimiento plan contra real.
- **Aviso obligatorio:** es una extensión pedida por Juan, no un método del diplomado, y no es garantía. Sin Search Console no se ejecuta.
- **Ejemplo:** `/aprendoclub project`
- **Salidas:** `proyeccion-gsc.json`.

## `/aprendoclub report <sitio>`

- **Ejecuta:** `reporte-seo-gsc` (Semana 12): resumen, rendimiento mes contra mes, ganadoras y próximos pasos con las 4 métricas de Search Console. Cierra con `dashboard-seo`.
- **Pide:** dos exports de Search Console (mes actual y anterior) o conexión por MCP.
- **Ejemplo:** `/aprendoclub report midominio.com`
- **Salidas:** `search-console.json`.

## `/aprendoclub proposal`

- **Ejecuta:** `propuesta-y-reporte-de-servicios-seo` (Semanas 2, 13 y 16): propuesta con los 3 pilares, paquetes Bronce/Plata/Oro, explainer y comunicación con el cliente. Tarifas y cifras que el usuario no dé quedan `pendiente de dato`.
- **Ejemplo:** `/aprendoclub proposal`

## `/aprendoclub dashboard`

- **Ejecuta:** `dashboard-seo`: une los `data/*.json` en una web local y entrega el URL. Pide el sitio si hay más de una carpeta en `.seo-audit/`.
- **Ejemplo:** `/aprendoclub dashboard`

## `/aprendoclub help`

Muestra la tabla de comandos de `SKILL.md`, cada uno con una línea. Sin argumentos es el comportamiento por defecto.
