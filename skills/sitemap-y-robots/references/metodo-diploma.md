# Método del diploma: sitemap y robots.txt (Semanas 3, 12 y 13)

> Fuente: resúmenes oficiales del diplomado "De Cero a SEO" (aprendoseo, Arianna Lupi), `data/diplomado/docs/`. No hay una lección dedicada solo a estos archivos: el tema aparece en cuatro lecciones, y esta skill las junta.

## Qué enseña el curso

**Semana 3 · "Cómo funciona Google" (Juan Carlos Angulo)**
- Tres etapas en secuencia: **rastreo, indexación y renderizado**. Metáfora del **turista y el mapa**.
- **Robots.txt:** "el manual de instrucciones que le dice al robot por qué calles puede pasar y cuáles tiene prohibidas".
- **Sitemap:** "el mapa oficial que le entregamos a Google para que encuentre todas nuestras páginas importantes".
- Tip: si bloqueas por error el sitio en el robots.txt, por muy buen contenido que tengas, "el turista nunca llegará a tu puerta".
- Acciones de Trello: crear la tarjeta "Ciclo de Google" (Rastreo, Indexación, Renderizado) y **buscar el sitemap** en `tudominio.com/sitemap.xml`.
- Prompt oficial: "Actúa como un Ingeniero SEO en aprendoseo. Explica las tres etapas críticas (Rastreo, Indexación y Renderizado) usando la metáfora del 'turista y el mapa'. Diseña un flujo de trabajo para verificar la salud del archivo robots.txt y del sitemap, asegurando que no existan barreras técnicas."

**Semana 3 · "Cuáles son las herramientas del SEO Técnico" y "Cómo aparecer en Google"**
- El operador `site:tudominio.com` muestra cuántas y cuáles páginas reconoce Google; **Search Console es la herramienta definitiva** para saber por qué una página no se indexa.
- Tres guardianes de la indexación: **robots.txt**, **etiquetas noindex** (útiles en páginas legales o de inicio de sesión) y **sitemap** actualizado.
- Si en `site:` aparecen carpetas de administración o archivos basura: señal de alerta. "Menos es más si lo que tienes indexado es de alta calidad."
- Acciones de Trello: ejecutar `site:`, **comparar páginas reales vs indexadas**, y revisar `tudominio.com/robots.txt` para asegurar que no aparezca `Disallow: /`.
- Prompt oficial: "Actúa como un Estratega de Visibilidad en aprendoseo. Usa el comando site: para auditar la brecha de indexación y revisa que el archivo robots.txt o etiquetas noindex no bloqueen secciones clave. Valida tu sitemap y genera un plan de acción en Google Search Console..."

**Semana 12 · "Indexabilidad y rastreabilidad" (Bloque 1 de la auditoría técnica)**
- Distinción **rastreabilidad** (los robots recorren el sitio por enlaces) vs **indexabilidad** (las páginas rastreadas entran al índice).
- Un 302 en el rastreo suele venir de un bloqueo en robots.txt. "Lo que no se rastrea, no existe."
- Acciones de Trello: simulacro de rastreo con Screaming Frog (Response Codes 4xx/5xx); **verificar el robots.txt** (sin `Disallow: /` en lo que quieres posicionar); **Sitemap Check** en Search Console (procesado recientemente, sin errores de lectura).
- Prompt oficial (Auditor de Infraestructura SEO): "Analiza mi archivo Robots.txt y mi Sitemap [enlaces] para asegurar que no estoy bloqueando por error secciones importantes y sugiere 3 acciones prioritarias para mejorar la velocidad de carga y la indexabilidad inmediata."

**Semana 13 · "El Rol del SEO Técnico: Detrás de Escena"**
- El SEO técnico no siempre arregla el código: **documenta el error y se lo explica al developer**. Prompt: redactar un ticket técnico claro dirigido a un programador (por qué afecta, recomendaciones como ajustes en `.htaccess` o `robots.txt`).

## Práctica de coaches (afina criterios, no sustituye el curso)

Fuente: `data/voice-profile.md` (Juan Angulo) y `data/coaches/vero.md`.

- **robots.txt es una guía para los bots, no una barrera;** pueden ignorarla. `Allow` desde `/` está bien; `crawl-delay` frena rastreos muy rápidos; hay sitios que bloquean bots como Screaming Frog por carga al servidor.
- **Probar el robots.txt** con `technicalseo.com/tools/robots-txt`.
- **Sitios con código (Next.js):** el sitemap y el robots los genera un developer; si dan 404 es porque faltan. Se le entrega documentación oficial (Next.js).
- **Cloudflare** suele inyectar reglas que bloquean crawlers de IA; se editan desde Cloudflare y una mala configuración puede evitar que las IAs indexen o mencionen el sitio. En el diagnóstico siempre se pregunta: "¿Estás usando Cloudflare?"
- **WordPress:** sitemaps con Rank Math o Yoast, no listas manuales. Con Divi, los parámetros `?et_blog` se resuelven con una regla en robots.txt.
- **Shopify:** el robots.txt sí es editable; el sitemap se crea solo y no se edita.
- **GSC:** "Descubierta, actualmente sin indexar" no significa que falte en el sitemap (se inspecciona la URL y en "páginas de referencia" casi siempre está). "Rastreada, sin indexar": revisa enlaces entrantes, sitemap, robots y canónica autorreferenciada.
- **Octopus:** el modo de IA inventa el mapa; para rastrear de verdad, `octopus.do/sitemap/generator` (hasta 500 URLs gratis).
- **Autor (E-E-A-T):** la sección `/author` no se bloquea en el robots.
- **Pedir evidencia antes de diagnosticar:** captura de Search Console, el robots.txt, el crawl.
- Vero: si el sitemap es un índice, cargar cada archivo por separado en Screaming Frog.

## Plantilla mínima de robots.txt (para entregar al developer)

```
User-agent: *
Allow: /
# Disallow: /ruta-privada/

Sitemap: https://dominio.com/sitemap.xml
```

Cualquier regla adicional se justifica por escrito: qué bloquea, por qué y qué URL de ejemplo queda afectada.
