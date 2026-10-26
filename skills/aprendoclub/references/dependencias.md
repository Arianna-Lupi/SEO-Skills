# Requisitos de los scripts: cómo se resuelven

Idea tomada de claude-seo (MIT): un lanzador estable que resuelve el intérprete y falla con un mensaje claro. Aquí, además, nada se instala sin permiso. Fuente de verdad: [`../requisitos.json`](../requisitos.json), validado por `scripts/validar_skills.py`.

## Intérprete (en este orden)

1. `APRENDOCLUB_PYTHON` (ruta a un ejecutable, Python 3.9 o superior).
2. `python3`, luego `python`, luego `py -3` en Windows. Se ignora el atajo falso de la Microsoft Store.
3. Para correr un script con paquetes: el intérprete anterior si ya los tiene; si no, el entorno aislado `~/.claude/aprendoclub/.venv` si existe.
4. `uv` solo se usa para crear ese entorno rápido (`uv venv`, `uv pip install`) cuando el usuario aprobó instalar. Si no hay Python, `needs` sugiere `uv python install` como alternativa.

## Contrato de salida

`aprendoclub-run --check <script>` devuelve siempre JSON y sale con 0, incluso cuando falta algo:

```json
{"ok": false, "script": "analisis-serp-y-competencia/serp.py",
 "needs": [
   {"type": "python_dep", "name": "requests", "required": true, "command": "aprendoclub-run --install analisis-serp-y-competencia/serp.py --yes"},
   {"type": "api_key", "name": "SERPAPI_API_KEY", "required": true, "where": "...", "fallback": "modo manual: ..."}],
 "reason": "faltan requisitos: requests, SERPAPI_API_KEY", "fallback": "modo manual: ..."}
```

- `ok` es `false` solo si falta algo con `required: true`. Lo opcional que falta aparece en `needs` con `required: false`, para ofrecerlo, pero no bloquea.
- `reason` y `fallback` mantienen el contrato antiguo de los scripts (`{"ok": false, "reason", "fallback"}`), así que quien ya lo lee sigue funcionando.
- Tipos: `python` (intérprete), `python_dep`, `api_key`, `tool` (por ejemplo Node o Screaming Frog).
- Correr un script sin pasar el chequeo (`aprendoclub-run <script>`) imprime ese mismo JSON y sale con 3, sin ejecutarlo.

## Reglas de seguridad

- `--install` exige `--yes` y solo instala paquetes que están en `paquetes` del manifiesto (lista cerrada). Nunca usa sudo ni toca el Python del sistema.
- Las claves se leen del entorno o de `~/.claude/seo-skills.env`; el chequeo solo dice si existen. Los valores nunca se imprimen ni van a `.seo-audit/`.
- El manifiesto solo contiene nombres de variables, jamás valores.
- Los scripts siguen siendo stdlib primero; no se añaden dependencias pesadas (nada de navegadores, generadores de PDF ni librerías de gráficos).
