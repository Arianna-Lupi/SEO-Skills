# Complementos de claude-seo para el enrutador

> **Complemento externo (claude-seo, MIT), no es parte del método del diplomado.** Patrones adaptados de https://github.com/AgriciDaniel/claude-seo (© 2026 agricidaniel). Licencia en `THIRD-PARTY-LICENSES.md`.

## Qué se tomó y cómo se adaptó

| Patrón de claude-seo | Archivo de origen | Adaptación en `/aprendoclub` |
|----------------------|-------------------|------------------------------|
| Un orquestador `/seo <comando> <argumento>` con tabla de comandos | `skills/seo/SKILL.md` | `/aprendoclub <comando> <argumento>`, con comandos y fases del diplomado en español |
| Auditoría que delega en subagentes en paralelo y recolecta resultados | `skills/seo/SKILL.md` (Orchestration Logic), `skills/seo-audit/SKILL.md` | `audit` con 9 fases; el paralelismo solo entre tareas independientes y con checkpoints humanos entre fases |
| Puntaje de salud de 0 a 100 | `skills/seo-audit/SKILL.md` | Se reutiliza `puntaje_salud.py` (ya en `auditoria-tecnica`) para comparar corridas; se aclara que no es un dato de Google |
| Subagentes condicionales según el tipo de negocio | `skills/seo/SKILL.md` | La fase 6 elige `seo-local` o `seo-ecommerce` según el tipo detectado en la fase 0 |
| Artefactos de salida por sitio | `skills/seo-audit/SKILL.md` | `.seo-audit/<sitio>/data/*.json` según la convención de `dashboard-seo` |

## Qué NO se tomó

- El runtime administrado (`bin/claude-seo`, entorno Python aislado, Chromium): las skills de este repo corren con stdlib y `uv` opcional.
- Hooks de validación, extensiones MCP de pago (DataForSEO y otras) y el marco de síntesis de 10 principios: sin base en el diplomado.
- Comandos sin skill equivalente en el diplomado (`drift`, `hreflang`, `programmatic`, `sxo`, `maps`): quedan como ideas en `ROADMAP.md`.
