---
name: configurar-serpapi
description: Usa esta skill cuando una skill SEO necesite datos en vivo de SerpApi (SERP real, People Also Ask, autocomplete, AI Overview) y NO haya una clave configurada, o cuando el usuario quiera conectar/activar SerpApi o dar su API key — aunque no diga "SerpApi", p.ej. "no tengo clave", "cómo consigo datos reales de Google", "quiero datos en vivo", "aquí está mi api key", "conecta SerpApi", "configura mi clave". Guía al usuario para crear una cuenta GRATIS en SerpApi (100 búsquedas/mes sin tarjeta), pide su API key, la guarda en ~/.claude/seo-skills.env y la valida, para que todas las skills la usen automáticamente en cada sesión sin volver a pedirla.
compatibility: Script opcional requiere Python 3 (uv) + requests solo para validar la clave. Guarda la clave en ~/.claude/seo-skills.env, que los scripts de SerpApi cargan solos. Alternativa: MCP de SerpApi (ver MCP-SETUP.md).
metadata:
  author: aprendoseo
  milestone: SEO skills (De Cero a SEO)
  version: "1.0"
---

> **🚫 Regla de datos (obligatoria): NUNCA inventes números ni claves.**
> No te inventes la API key ni ningún dato. La clave la da SIEMPRE el usuario desde su cuenta de SerpApi. Si no la tiene, guíalo a crearla; nunca la supongas ni la dejes en blanco para "seguir".

# Configurar SerpApi (datos en vivo para las skills)

Actúa como asistente de configuración en aprendoseo. Varias skills (`analisis-serp-y-competencia`, `investigacion-de-keywords`, `brief-de-contenido`, `optimizacion-geo-aeo`) y los agentes funcionan en **modo manual sin nada**, pero rinden mucho más con datos en vivo de Google vía **SerpApi**. SerpApi tiene un **plan gratuito (100 búsquedas/mes, sin tarjeta)**, suficiente para empezar. Tu trabajo: que el usuario tenga su clave guardada **una vez** y que todas las skills la usen **siempre**.

## Cuándo usar

- Una skill devolvió `Falta SERPAPI_API_KEY` (o un script salió en modo manual por falta de clave).
- El usuario dice que quiere datos reales de la SERP / PAA / autocomplete, o "no tengo clave".
- El usuario pega una API key en el chat o pide "conectar/configurar SerpApi".

## Proceso

1. **Explica y manda crear la cuenta gratis.** Dile, textual y con el enlace:
   > Crea una cuenta gratis en SerpApi: **https://serpapi.com/users/sign_up** (100 búsquedas/mes, sin tarjeta). Luego copia tu clave desde **https://serpapi.com/manage-api-key** y pégala aquí.

2. **Pide la clave y espera.** No continúes hasta que el usuario la pegue. NUNCA la inventes.

3. **Avísale del riesgo mínimo de seguridad.** Pegar una clave en el chat la deja en la conversación. Es una clave de solo-lectura de búsquedas y se puede regenerar en SerpApi cuando quiera. Se guardará **localmente** en `~/.claude/seo-skills.env` con permisos `600` (solo su usuario) y **no** se sube al repo ni a ningún lado.

4. **Guárdala y valídala** con el script (no imprime la clave completa, solo los últimos 4 caracteres):
   ```bash
   uv run set_key.py --key "LA_CLAVE_QUE_PEGO" --test
   ```
   - `--test` consulta la cuenta de SerpApi (no gasta búsquedas) y devuelve si es válida y cuántas búsquedas le quedan.
   - Si el usuario prefiere no dejarla en el comando: `--key -` y que la pegue por stdin.

5. **Confirma.** Si `test.valid` es `true`, dile que ya quedó: todas las skills la tomarán sola en esta y futuras sesiones. Si es `false` (401), la clave está mal: que la copie de nuevo desde el panel.

6. **(Opcional) MCP.** Si además quiere el MCP de SerpApi (para que el modelo lea SERPs directamente sin script), remítelo a `MCP-SETUP.md`. El MCP y la clave de los scripts son independientes; tener ambos no estorba.

## Salida

Un mensaje breve confirmando: clave guardada (enmascarada), válida sí/no, búsquedas restantes, y que las skills ya la usan. No repitas la clave completa.

## Cómo la usan las demás skills

Los scripts `serp.py`, `expand_keywords.py`, `serp_outline.py` y `ai_features.py` cargan `~/.claude/seo-skills.env` automáticamente antes de leer `SERPAPI_API_KEY`. No hay que exportar nada en cada terminal ni reinstalar: se guarda una vez y queda.

## Ejemplo

Usuario: *"quiero datos reales, no tengo clave"*.
1. Le pasas el enlace de registro y el de la API key.
2. Pega: `abc123...def`.
3. Le recuerdas el tema de seguridad (queda local, 600, regenerable).
4. `uv run set_key.py --key "abc123...def" --test` → `{"ok": true, "masked": "…0def", "test": {"valid": true, "plan_searches_left": 100}}`.
5. Confirmas: *"Listo, clave válida (100 búsquedas/mes). Las skills ya la usan solas."*

## Script determinista (ahorro de tokens)

`scripts/set_key.py` — guarda/actualiza la variable en `~/.claude/seo-skills.env` (conserva otras), `chmod 600`, enmascara la clave en la salida y valida con `--test` sin gastar búsquedas. Stdlib (+ requests solo para `--test`).
