# Rúbrica de clasificación de riesgo de backlinks

Criterios exactos y reproducibles para asignar una de 4 categorías de riesgo a cada dominio referente. Implementados en `scripts/classify_domains.py`. Origen: metodología validada en una auditoría real (sector retail de nicho, cientos de dominios y miles de backlinks analizados).

## Las 4 categorías

### 1. Toxic

Cumple **cualquiera** de estas dos condiciones:

**(a) Disparador automático ("granja de enlaces"):**
`external_links > 1000` en la página de origen **Y** `sitewide = true` **Y** país sin relación con el mercado del cliente (país vacío cuenta como no relacionado).

**(b) Ascore bajo + señal de riesgo adicional:**
`domain_ascore <= 2` **Y** al menos una señal adicional genuina: `sitewide`, `external_links > 1000`, o anchor comercial/exacto repetido en más de 5 dominios distintos.

**Nunca** se marca Toxic por ascore solo ni por país solo — evita falsos positivos de sitios nuevos legítimos.

### 2. Suspicious

No califica Toxic pero cumple cualquiera de:
- `ascore <= 2` sin otra señal (ascore bajo solo).
- Anchor comercial repetido en masa, sin el resto de condiciones de Toxic.
- Solo UNA de las dos condiciones del disparador automático de Toxic (patrón de granja parcial).

### 3. Low-quality-but-safe

No califica Toxic ni Suspicious y cumple:
- `ascore` entre 3 y 5 sin ninguna otra señal de riesgo, **o**
- `external_links` moderado (por encima de lo típico de una página normal, sin llegar al umbral de 1000) sin sitewide ni anchor en masa.

### 4. Neutral-OK

No califica en ninguna de las 3 anteriores: perfil limpio, sin señales de riesgo detectadas.

## Reglas de manejo de datos (no negociables)

- **País vacío es señal neutra.** Nunca dispara Suspicious ni Toxic por sí solo — siempre requiere una señal co-ocurrente (sitewide, external>umbral, o anchor en masa) para escalar. Descartar un dominio solo por el país es el error más común de rúbricas caseras: produce falsos positivos masivos en países con poca cobertura de datos.
- **Análisis domain-first, propagación a backlinks individuales.** Clasificas a nivel de dominio primero, luego heredas la categoría a cada backlink de ese dominio. Excepción caso a caso: si un backlink individual diverge claramente del patrón de su dominio (ej. dominio Neutral-OK pero una página específica tiene external>1000 + sitewide), marca ese backlink con override y sube su categoría un nivel — sin tocar la categoría general del dominio.
- **Consolida duplicados exactos** (mismo origen + mismo destino, distinto first/last seen) en una sola fila con `instance_count`.
- **Nofollow desde dominio tóxico se incluye igual** en la clasificación y en el disavow — el atributo `nofollow` no protege del todo contra el efecto de un enlace tóxico. Prefiere prolijidad/exhaustividad sobre omisión.
- **Cada fila necesita evidencia citable.** La columna `evidencia` debe nombrar la regla exacta aplicada — es lo que hace la clasificación auditable y defendible frente al cliente.

## Adaptar los umbrales

Los umbrales (`external_links > 1000`, `ascore <= 2`, rango 3-5, país "relacionado") vienen de un caso real y son punto de partida razonable, no dogma. Ajústalos si el sitio del cliente tiene un perfil de backlinks atípico (ej. nicho ultra-local con pocos dominios de referencia, o sitio internacional donde "país relacionado" no aplica) — documenta el cambio y el motivo en el propio informe.
