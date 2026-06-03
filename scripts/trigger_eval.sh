#!/usr/bin/env bash
#
# trigger_eval.sh — Pruebas de activación (trigger evals) para Skills.
#
# Adaptado de la guía "Optimizing skill descriptions" de agentskills.io:
#   https://agentskills.io/skill-creation/optimizing-descriptions
#
# Mide si la `description` de una Skill hace que el modelo la ACTIVE ante
# prompts realistas (should_trigger:true) y que NO la active ante near-misses
# que pertenecen a otra Skill (should_trigger:false).
#
# Uso:
#   bash scripts/trigger_eval.sh <eval_queries.json> <SKILL_NAME> [runs]
#
# Ejemplo:
#   bash scripts/trigger_eval.sh skills/brief-de-contenido/evals/eval_queries.json brief-de-contenido 3
#
# Argumentos:
#   <eval_queries.json>  Archivo con [{ "query": "...", "should_trigger": true|false }, ...]
#   <SKILL_NAME>         Nombre de la skill (== carpeta y campo `name` del SKILL.md)
#   [runs]              Veces que se corre cada query (default: 3). La activación
#                       del LLM es estocástica; promediar reduce el ruido.
#
# Detección: se ejecuta `claude -p "$query" --output-format json` y, con jq, se
# busca en los mensajes un bloque tool_use cuyo name=="Skill" cuya entrada
# referencie a SKILL_NAME. Si aparece al menos una vez en los `runs`, la query
# se considera ACTIVADA en esa corrida.
#
# Métrica: trigger_rate = (corridas con activación) / (total de corridas) por query.
#   - Para should_trigger:true  → queremos trigger_rate ALTO  (≥ 0.5 = PASS).
#   - Para should_trigger:false → queremos trigger_rate BAJO  (< 0.5 = PASS, near-miss no debe disparar).
# UMBRAL DE APROBACIÓN: 0.5. Una query falla si cae del lado equivocado del 0.5.
#
# Train / validation split: separá tus queries 60/40. Iterá la `description`
# SOLO contra el set de TRAIN (~60%) y, recién cuando pase, validá una única vez
# contra el set de VALIDATION (~40%) que nunca usaste para ajustar. Así evitás
# sobreajustar la descripción a tus propios ejemplos. La guía sugiere ~5
# iteraciones de refinamiento sobre train antes de tocar validation.
#
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Uso: bash scripts/trigger_eval.sh <eval_queries.json> <SKILL_NAME> [runs]" >&2
  exit 1
fi

EVAL_FILE="$1"
SKILL_NAME="$2"
RUNS="${3:-3}"
THRESHOLD="0.5"

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: se requiere jq." >&2
  exit 1
fi
if ! command -v claude >/dev/null 2>&1; then
  echo "Error: se requiere el CLI 'claude'." >&2
  exit 1
fi
if [[ ! -f "$EVAL_FILE" ]]; then
  echo "Error: no existe $EVAL_FILE" >&2
  exit 1
fi

# Detecta si la herramienta Skill se disparó para SKILL_NAME en una salida JSON de claude.
# Devuelve "1" si activó, "0" si no.
detect_trigger() {
  local output="$1"
  echo "$output" | jq -r --arg skill "$SKILL_NAME" '
    [ .. | objects
      | select(.type? == "tool_use" and .name? == "Skill")
      | (.input | tostring)
      | select(test($skill; "i"))
    ] | if length > 0 then "1" else "0" end
  ' 2>/dev/null | grep -qx "1" && echo "1" || echo "0"
}

results="[]"
n=$(jq 'length' "$EVAL_FILE")

for ((i = 0; i < n; i++)); do
  query=$(jq -r ".[$i].query" "$EVAL_FILE")
  should=$(jq -r ".[$i].should_trigger" "$EVAL_FILE")

  triggered_count=0
  for ((r = 0; r < RUNS; r++)); do
    out=$(claude -p "$query" --output-format json 2>/dev/null || echo '{}')
    if [[ "$(detect_trigger "$out")" == "1" ]]; then
      triggered_count=$((triggered_count + 1))
    fi
  done

  rate=$(echo "scale=4; $triggered_count / $RUNS" | bc)
  # PASS: should_trigger=true  → rate >= 0.5 ; should_trigger=false → rate < 0.5
  if [[ "$should" == "true" ]]; then
    pass=$(echo "$rate >= $THRESHOLD" | bc)
  else
    pass=$(echo "$rate < $THRESHOLD" | bc)
  fi
  [[ "$pass" == "1" ]] && pass_bool="true" || pass_bool="false"

  results=$(echo "$results" | jq \
    --arg q "$query" \
    --argjson should "$should" \
    --argjson rate "$rate" \
    --argjson pass "$pass_bool" \
    '. + [{query: $q, should_trigger: $should, trigger_rate: $rate, pass: $pass}]')
done

passed=$(echo "$results" | jq '[.[] | select(.pass)] | length')

jq -n \
  --arg skill "$SKILL_NAME" \
  --argjson runs "$RUNS" \
  --argjson threshold "$THRESHOLD" \
  --argjson total "$n" \
  --argjson passed "$passed" \
  --argjson results "$results" \
  '{
    skill: $skill,
    runs_per_query: $runs,
    threshold: $threshold,
    total_queries: $total,
    passed: $passed,
    pass_ratio: ($passed / $total),
    results: $results
  }'
