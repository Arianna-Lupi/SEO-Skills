# Complementos de claude-seo para link building

> **Complemento externo (claude-seo, MIT, agricidaniel), no es parte del método del diplomado.**

## Seguimiento automático de enlaces

`scripts/verificar_enlaces.py` (stdlib, respeta robots.txt, 1 petición por segundo, máximo 200 URLs) comprueba cada URL del Planificador: si el enlace sigue publicado, el anchor real, el `rel` (nofollow, sponsored, ugc) y si coincide con el anchor pactado. Es el paso "Seguimiento" de S12 L5 hecho verificable. Un `error` puede ser un WAF: revisa a mano.

## Fuentes gratuitas para el análisis de brecha

Si el cliente no tiene Ahrefs (de pago), estas fuentes dan pistas, con cobertura menor:

| Fuente | Qué da | Límite |
|---|---|---|
| Bing Webmaster Tools | Enlaces entrantes y dominios de TU sitio verificado | Solo sitios verificados, índice de Bing |
| Moz API (registro gratis) | DA/PA, dominios referentes, anchors | Cupo mensual pequeño; verifica los límites vigentes |
| Common Crawl (grafo web público) | Ranking y centralidad a nivel de dominio | Sin anchors ni páginas, trimestral |
| Verificación propia | Confirmar enlaces conocidos | Solo URLs que ya conoces |

Para comparar con competidores arbitrarios, estas fuentes gratuitas no bastan; usa un export de Ahrefs o Semrush. Los scripts de claude-seo (`bing_webmaster.py`, `commoncrawl_graph.py`, `moz_api.py`) requieren `requests` y claves; no se portaron porque el diplomado no los enseña.

## Descartado

- DataForSEO para backlinks nuevos y perdidos: de pago y fuera del diplomado.
- Tácticas de enlaces masivos o automatizados: el curso insiste en relaciones reales (S12 L5, S14 L11).
