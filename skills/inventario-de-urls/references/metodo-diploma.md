# Método del diploma: inventario de URLs (Semana 5 y Semana 3)

> Fuente: resúmenes oficiales del diplomado "De Cero a SEO" (aprendoseo, Arianna Lupi), `data/diplomado/docs/`.

## Qué enseña el curso

**Semana 5 · "Cómo obtener las URLs de un sitio web" (Verónica Romero)**

- Antes de asignar palabras clave necesitas la **lista completa de URLs** del sitio: "no podemos optimizar lo que no sabemos que existe". Al extraerlas aparecen páginas "olvidadas" que pueden estar afectando el SEO o tener potencial.
- **Screaming Frog** es la herramienta recomendada y estándar de SEO técnico: rastrea como Google y exporta la columna Address/URL en una lista limpia. Las extensiones de navegador (por ejemplo Link Klipper) sirven, pero entregan la lista más desordenada.
- Proceso: introduces el dominio, dejas que el robot rastree todo, exportas la columna de direcciones.
- La versión gratuita permite **hasta 500 URLs** por rastreo.
- La lista limpia va a la **Plantilla Master** y es la base del Mapa de Palabras Clave. Aguas abajo (S5 · "Cómo evaluar si las páginas tienen valor SEO") se decide cuáles URLs conservar.

**Prompt oficial (S5 · video 3):** "Actúa como un Estratega SEO Técnico en aprendoseo. Ayúdame a realizar la extracción completa de las URLs de mi proyecto. Guíame paso a paso para utilizar Screaming Frog (u otras alternativas como el sitemap XML) para obtener el listado de todas las direcciones de mi sitio. Enséñame a limpiar y organizar esta lista en mi Plantilla Master para que cada URL sea la base de mi futuro Mapa de Palabras Clave."

**Semana 3 · "Cómo funciona Google" y "Cómo aparecer en Google":** el sitemap es "el mapa oficial" que se entrega a Google (se busca en `tudominio.com/sitemap.xml`), y el operador `site:` mide la brecha entre lo que tú sabes que existe y lo que Google tiene indexado. Acción del curso: comparar el número de páginas reales vs el que muestra Google.

**Semana 3 · "Cómo ver la estructuración del sitio":** Screaming Frog también detecta **páginas huérfanas** (sin enlaces entrantes); el sitemap por sí solo no las muestra.

## Práctica de coaches (afina criterios)

- **Vero (S5):** rastrear el dominio en modo **Spider**, no cargando el sitemap, para no perder URLs; si el sitemap es un **índice**, cargar cada archivo por separado; en WordPress, quitar `wp-sitemap.xml` de la URL y dejar solo el dominio si Screaming Frog devuelve una sola URL.
- **Ibra:** sacar las URL del sitemap o filtrar por HTML en Screaming Frog; no descartar páginas con valor SEO y anotar por qué se descarta cada una.
- **Juan:** Octopus rastrea de verdad en `octopus.do/sitemap/generator` (hasta 500 URLs gratis); su modo de IA inventa el mapa. En Shopify el sitemap se genera solo y no se edita.
