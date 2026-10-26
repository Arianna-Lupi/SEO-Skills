#!/usr/bin/env bash
# Ejemplo de punta a punta SIN red, con las fixtures sintéticas (dominios .test, nada real).
# Uso: bash fixtures/ejecutar_ejemplo.sh [carpeta_salida]
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
SCR="$AQUI/../scripts"
OUT="${1:-/tmp/serp-ejemplo}"
H="$AQUI/html"
mkdir -p "$OUT"
python3 "$SCR/perfil_competidor.py" \
  --serp-json "$AQUI/serp_preparar_cafe.json" "$AQUI/serp_comprar_cafe.json" "$AQUI/serp_cafe_en_grano.json" \
  --sin-red \
  --html "https://cafeguia.test/blog/como-preparar-cafe=$H/competidor-guia.html" \
         "https://tazadiaria.test/blog/metodos-cafe=$H/competidor-metodos.html" \
         "https://cafelab.test/aprende/preparar-cafe=$H/competidor-spa.html" \
         "https://tostadores.test/tienda/cafe-de-especialidad/=$H/competidor-categoria.html" \
         "https://granoalto.test/categoria/cafe-de-especialidad/=$H/competidor-categoria-2.html" \
         "https://tostadores.test/producto/etiopia-yirgacheffe=$H/competidor-producto.html" \
  --own-html "$H/propio-blog.html" --out "$OUT/perfiles.json" > /dev/null
python3 "$SCR/comparar_serp.py" "$OUT/perfiles.json" --out "$OUT/comparacion.json" --md "$OUT/reporte.md" \
  --competitors-json "$OUT/data/competitors.json" > /dev/null
echo "Listo: $OUT/perfiles.json, $OUT/comparacion.json, $OUT/reporte.md, $OUT/data/competitors.json"
