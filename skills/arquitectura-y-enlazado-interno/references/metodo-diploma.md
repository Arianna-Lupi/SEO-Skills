# Método del diploma — Arquitectura web y enlazado interno (Semana 9, Arianna Lupi / Juan Carlos Angulo / Verónica Romero)

> Fuente: corpus interno "De Cero a SEO" (chunks, doc_type resumenes-prompts/transcripciones), Semana 9. Material de aprendoseo.

La Semana 9 cubre **Arquitectura Web** (Juan Carlos Angulo) y **Enlazado Interno** (Verónica Romero). Mensaje rector: *"Hazlo sencillo para el Crawler"* — si a Google le cuesta llegar a una página enterrada, no la posiciona.

## El método paso a paso (como lo enseña el curso)

**A. Diseñar la arquitectura** (videos 2-3)
1. Sostén la arquitectura sobre **3 pilares**: jerarquía clara (categorías = páginas padre, subcategorías = páginas hijo), enlaces internos y **URLs semánticas**.
2. Aplica la **regla de los 3 clics**: cualquier contenido importante debe estar a **máximo 3 clics desde el Home**. Más enterrado = Google no lo indexa bien y el usuario se rinde.
3. Equilibra **Crawl Depth** (profundidad: clics desde la Home, no superar 3 niveles) y **Crawl Width** (anchura: páginas por nivel; demasiada anchura sin jerarquía diluye autoridad).
4. Diseña primero "en papel"/digital, no en la web: define categorías por temas lógicos y keywords de alto volumen, luego subcategorías dependientes.
5. Diagrama el sitemap visual en **Octopus.do** (gratis); usa **Screaming Frog** para el análisis técnico masivo (404, niveles de profundidad).
6. Mantén las URLs semánticas: `/curso-seo/` en vez de `/p=123/` — "deben tener sentido tanto para nosotros, los usuarios, como para Google".

**B. Analizar la arquitectura existente** (video 6)
1. Mapea el sitio en Octopus.do; identifica páginas a más de 3 clics del Home.
2. Detecta errores: páginas innecesarias en el flujo principal (Login, Home repetido), falta de niveles intermedios (Home→producto sin categoría), y **páginas huérfanas**.
3. Escribe al menos **3 mejoras concretas** antes de tocar el código: *"Analiza antes de cambiar."*

**C. Enlazado interno** (videos 4-5)
1. Define el enlazado **desde el brief** (Semana 8), no después de publicar: "no esperes a que el contenido esté publicado para pensar en el enlazado".
2. Usa los **4 tipos de enlace interno** según su función (ver tabla).
3. Conecta las **páginas huérfanas** (sin ningún enlace interno entrante).
4. Dirige los enlaces a las **páginas pilares** para que reciban más Link Equity.
5. Usa **anchor text descriptivo** con la keyword; evita el genérico "haz clic aquí".

## Plantillas, criterios y umbrales exactos

| Concepto | Criterio del diploma |
|----------|----------------------|
| **Regla de los 3 clics** | Todo contenido importante ≤ **3 clics desde el Home** (en el prompt de diseño avanzado se pide apuntar a páginas pilares a **máx. 2 clics**) |
| **Crawl Depth** | Profundidad en clics desde la Home; **no superar 3 niveles** |
| **Crawl Width** | Cantidad de páginas en un mismo nivel; demasiada anchura sin jerarquía **diluye la autoridad** |
| **URL semántica** | Descriptiva y clara para usuario y Google (ej. `/curso-seo/`, no `/p=123/`) |
| **Página huérfana** | Página **sin enlaces internos entrantes**; hay que detectarla y conectarla |
| **Anchor text** | Descriptivo, con keyword; nunca "haz clic aquí" |
| **Enlace interno mínimo por pieza (brief)** | Al menos **2 enlaces contextuales** a otros artículos + **1 enlace a un producto/servicio** |

**Los 4 tipos de enlace interno (Verónica Romero, video 5):**

1. **Contextuales** — los más comunes y naturales; dentro del cuerpo del texto, hacia contenido relacionado (blog → blog).
2. **De contenido a producto/servicio** — conectan artículos informativos con páginas transaccionales; cruciales para la conversión.
3. **De producto a producto (cross-selling)** — recomiendan artículos complementarios; suben el ticket promedio y ayudan a Google a entender relaciones.
4. **De navegación (Menú y Footer)** — Menú/cabecera: categorías principales. Footer: legales, mapa del sitio y accesos a colecciones clave.

## Prompts originales que da el curso (verbatim)

**Auditor de Jerarquía Web (Semana 9, video 2):**
> "Actúa como Consultor de Arquitectura SEO en aprendoseo. Analiza la estructura actual de mi sitio para aprendoseo y dime si cumple con la regla de los 3 clics. Sugiere cómo reorganizar mis categorías y subcategorías para reducir la profundidad de clics y mejorar la distribución de autoridad mediante enlaces internos."

**Diseñador de Mapas de Sitio SEO (Semana 9, video 3):**
> "Actúa como Arquitecto de Información en aprendoseo. Basado en mi lista de keywords para aprendoseo, propón una estructura de categorías y subcategorías lógica. Organiza el contenido de forma que las páginas pilares estén a un máximo de 2 clics del inicio y define qué temas deberían agruparse en cada sección para maximizar el rastreo."

**Especialista en Tipos de Enlaces (Semana 9, video 5):**
> "Actúa como Arquitecto de Conversión en aprendoseo. Analiza mi contenido de aprendoseo y propón un esquema de enlazado interno que combine: 1) Enlaces contextuales entre blogs, 2) Enlaces de blog a producto para convertir, y 3) Una estructura de footer que facilite la navegación y mejore el rastreo de Google."

**Auditor de Eficiencia Arquitectónica (Semana 9, video 6):**
> "Actúa como Consultor SEO Técnico en aprendoseo. Ayúdame a analizar la arquitectura de aprendoseo. Utiliza los conceptos de Crawl Depth y Crawl Width para identificar páginas 'enterradas' y sugiere 3 mejoras específicas para simplificar la jerarquía y asegurar que los buscadores encuentren mi contenido más valioso."

## Términos del diploma (definiciones)

- **Arquitectura web:** el "esqueleto" / diseño de la estructura del sitio; jerarquía + enlaces + URLs. Una mala planificación puede hacer que hasta el 60% de páginas importantes nunca se encuentren.
- **Crawl Depth (profundidad):** número de clics desde la Home hasta una página.
- **Crawl Width (anchura):** cantidad de páginas en un mismo nivel jerárquico.
- **Regla de los 3 clics:** todo contenido importante a ≤ 3 clics del Home.
- **Link Equity ("jugo SEO"):** la "fuerza"/autoridad que un enlace interno transfiere de una página a otra. Los enlaces internos hacen que el jugo fluya hacia páginas nuevas o secundarias.
- **Página huérfana:** página que no recibe ningún enlace interno.
- **Enlace interno vs externo:** interno conecta tu propio contenido (guía y distribuye autoridad); externo apunta a otro sitio (backlink si alguien te enlaza).
- **URL semántica:** dirección descriptiva, con sentido para usuario y Google.

## Ejemplos del curso

- **"El enlazado interno es el pegamento de tu web" (S9 chunk 4):** un sitio sin enlaces internos es "como una ciudad sin calles"; por bueno que sea el contenido, sin caminos Google y los usuarios lo ignoran.
- **Página huérfana (S9 transcripción):** "páginas que no tienen enlaces internos hacia ellas"; en Screaming Frog se revisa la pestaña de links internos para ver cuáles páginas tienen más/menos enlaces.
- **URLs limpias (S9 transcripción):** "las URLs deben ser semánticas y claras... que deben tener sentido tanto para nosotros como los usuarios como para Google."
- **Errores de arquitectura comunes (S9 chunk 6):** páginas de Login/Home repetidas ensuciando la jerarquía, falta de categorías intermedias y páginas huérfanas.
- **Enlace contextual (S9 transcripción):** de un post de "Email Marketing" a uno de "Optimización de campañas" — el tipo más común y útil.
