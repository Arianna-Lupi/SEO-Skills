# Conectar MCPs (opcional): guía para el equipo

Esto es totalmente opcional. Las skills y agentes de esta carpeta funcionan sin conectar nada: pegas los datos (un export de Search Console, un pantallazo o JSON de la SERP, tu lista de keywords) y la skill trabaja igual.

Conectar un MCP solo sirve para una cosa: que Claude vaya a buscar esos datos en vivo por su cuenta, en vez de que tú los pegues a mano.

¿Qué es un MCP? Las siglas son Model Context Protocol. Piénsalo como un enchufe estándar que le da a Claude acceso a una herramienta de afuera (SerpApi, Ahrefs, etc.). Una vez enchufado, Claude puede pedirle datos a esa herramienta solo.

Este es el orden en que conviene conectarlos, si decides hacerlo:

| MCP | Costo | Para qué | Prioridad |
|-----|-------|----------|-----------|
| **SerpApi** | **GRATIS** (~100 búsquedas/mes en el plan free) | SERP en vivo, "People Also Ask", búsquedas relacionadas, autocompletar | **Principal — conecta este primero** |
| **Ahrefs** | **PAGO** (suscripción Ahrefs con API, plan alto) | Volumen, dificultad (KD), backlinks, auditoría de sitio, datos de GSC | Opcional, si el equipo ya paga Ahrefs |
| **Google Search Console** (`mcp-gsc`) | **GRATIS** (MCP comunitario open-source) | Clics, impresiones, CTR, posición, inspección de URLs, sitemaps (reportes + cobertura) | Opcional — `AminForou/mcp-gsc` vía `uvx` |

---

## 0. Lo que necesitas antes de empezar

Ten Claude Code instalado y la sesión iniciada. Para iniciar sesión:

```bash
claude login
```

En cualquier momento puedes revisar qué MCPs ya están conectados:

```bash
claude mcp list
```

Y si estás dentro de una sesión de Claude Code, escribe `/mcp` para ver lo mismo.

---

## 1. SerpApi (gratis, el principal)

SerpApi te da un servidor MCP remoto con una URL propia, que lleva tu token adentro (un token es una clave secreta que te identifica).

Pasos:

1. Crea una cuenta gratis en https://serpapi.com y copia tu API token desde https://serpapi.com/manage.
2. Arma tu URL personal pegando el token en el medio: `https://mcp.serpapi.com/TU_TOKEN/mcp`
3. Conéctalo a Claude Code. El scope `user` quiere decir que queda disponible en todos tus proyectos, no solo en este:

   ```bash
   claude mcp add --transport http serpapi \
     https://mcp.serpapi.com/TU_TOKEN/mcp --scope user
   ```

4. Comprueba que quedó conectado:

   ```bash
   claude mcp list      # debería listar "serpapi"
   ```
   También sirve `/mcp` dentro de la sesión.

El plan free te da unas 100 búsquedas al mes (mira el límite actual en la página de precios de SerpApi). Alcanza de sobra para análisis puntuales de SERP o de "People Also Ask".

> ⚠️ **No publiques tu token.** Si lo conectas con `--scope project`, el token queda escrito en el archivo `.mcp.json` del repo, y lo ve cualquiera que tenga acceso al repo. Para uso personal usa siempre `--scope user`.

Con SerpApi conectado, skills como `analisis-serp-y-competencia`, `brief-de-contenido` y `optimizacion-on-page-meta` pueden traer la SERP y el "People Also Ask" reales, sin que los pegues a mano.

---

## 2. Ahrefs (pago)

> Esto **requiere una suscripción Ahrefs con acceso a API**, que es uno de los planes caros. Si el equipo no paga Ahrefs, sáltalo sin problema: las skills igual funcionan. Pegas los datos a mano, o usas las alternativas gratuitas que cada skill menciona (DinoRank, la versión free de Ahrefs, Google Keyword Planner, etc.).

Ahrefs no tiene un servidor MCP que instales con un comando. Se conecta de otra forma, como conector dentro de claude.ai:

1. Ten tu cuenta de Ahrefs con la API habilitada.
2. Inicia sesión en Claude Code con tu cuenta de Claude.ai (`claude login`).
3. Ve a https://claude.ai/customize/connectors, elige Ahrefs y autentica con tu cuenta de Ahrefs.
4. Vuelve a Claude Code y corre `/mcp` para confirmar que aparece el conector de Ahrefs.

Una vez conectado, las skills que piden volumen, KD, backlinks o auditoría (`investigacion-de-keywords`, `mapa-de-palabras-clave`, `auditoria-tecnica`, `arquitectura-y-enlazado-interno`, `reporte-seo-gsc`) usan datos reales de Ahrefs.

---

## 3. Google Search Console con el MCP `mcp-gsc` (gratis, comunitario)

Hay un MCP de GSC de código abierto y gratuito: `AminForou/mcp-gsc` (https://github.com/AminForou/mcp-gsc). Trae los datos de Search Console en vivo (queries, clics, impresiones, CTR, posición, inspección de URLs, sitemaps, comparación entre periodos). Es ideal para la skill `reporte-seo-gsc` y para la cobertura de indexación en `auditoria-tecnica`.

Es un programa hecho en Python que se corre con `uvx`, y se comunica con Claude por stdio (la entrada y salida de texto del propio programa). Pasos:

1. Instala `uv`, que es el gestor de paquetes de Python que vamos a usar:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env
   ```
2. Consigue credenciales de Google. Tienes dos caminos, elige uno:
   - **OAuth (recomendado):** OAuth es el sistema de Google para darle permiso a una app sin compartir tu contraseña. Descarga el `client_secrets.json` desde Google Cloud Console (la primera vez te abre el navegador para que inicies sesión).
   - **Cuenta de servicio:** una cuenta de servicio es un "usuario robot" de Google. Descarga su `service_account.json` y agrega el email de esa cuenta como usuario con acceso a tu propiedad de GSC. *(Ya tenemos una cuenta de servicio de Google en el proyecto, así que se puede reutilizar.)*
3. Conéctalo a Claude Code (scope `user`). Usa el bloque que corresponda al camino que elegiste:
   ```bash
   # OAuth:
   claude mcp add --transport stdio gsc --scope user \
     --env GSC_OAUTH_CLIENT_SECRETS_FILE=/ruta/a/client_secrets.json \
     -- uvx mcp-search-console

   # o Cuenta de servicio:
   claude mcp add --transport stdio gsc --scope user \
     --env GSC_CREDENTIALS_PATH=/ruta/a/service_account.json \
     --env GSC_SKIP_OAUTH=true \
     -- uvx mcp-search-console
   ```
4. Compruébalo con `claude mcp list` o con `/mcp`.

Si usas Claude Desktop en lugar de Claude Code, el equivalente en `claude_desktop_config.json` es:
```json
{
  "mcpServers": {
    "gscServer": {
      "command": "/RUTA/COMPLETA/A/uvx",
      "args": ["mcp-search-console"],
      "env": { "GSC_OAUTH_CLIENT_SECRETS_FILE": "/ruta/a/client_secrets.json" }
    }
  }
}
```

Otras maneras de traer datos de GSC, por si esta no te sirve:
- **Vía Ahrefs (pago):** el conector de Ahrefs trae endpoints `gsc-*` si tu cuenta los tiene vinculados.
- **Export manual (gratis, sin instalar nada):** descargas el CSV de Rendimiento desde GSC y lo pegas. La skill `reporte-seo-gsc` (y su script `gsc_report.py`) lo interpreta igual.

> Confirma el nombre del paquete (`mcp-search-console`) y las variables de entorno en el README de `AminForou/mcp-gsc`, por si cambian.

---

## 4. Cómo usan esto las skills

Ninguna skill te obliga a conectar un MCP. Todas siguen el mismo patrón, y cada una lo explica en su sección "Datos (MCP opcional)":

- **Sin MCP:** pegas los datos (keywords, SERP, export de GSC) y la skill trabaja igual, solo que con datos que tú cargaste.
- **Con SerpApi (gratis):** trae SERP, PAA y autocompletar en vivo.
- **Con Ahrefs (pago):** trae volumen, KD, backlinks, auditoría y GSC.

Conectarlos es una comodidad para tener datos frescos, no un requisito.

---

## Comandos a mano para tener cerca

```bash
claude mcp list                 # ver MCPs conectados
claude mcp get serpapi          # detalle de uno
claude mcp remove serpapi       # quitar uno
/mcp                            # estado en vivo dentro de la sesión
```

Si quieres compartir la conexión con el equipo a través del repo, este es el formato de un `.mcp.json` a nivel proyecto. Recuerda que el token queda a la vista de todos:

```json
{
  "mcpServers": {
    "serpapi": {
      "type": "http",
      "url": "https://mcp.serpapi.com/TU_TOKEN/mcp"
    }
  }
}
```

Docs oficiales: Claude Code MCP (https://code.claude.com/docs/en/mcp-servers), SerpApi (https://serpapi.com/manage), conectores de claude.ai (https://claude.ai/customize/connectors).

> Los límites del plan free de SerpApi y la disponibilidad de conectores pueden cambiar, así que revísalos en sus páginas oficiales.
