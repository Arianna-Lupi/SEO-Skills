# Complementos de claude-seo para auditoría de backlinks

> **Complemento externo (claude-seo, MIT, agricidaniel), no es parte del método del diplomado.** Rangos y listas son heurísticas de terceros: sirven para levantar banderas, no para sentenciar.

## Perfil de anclas (script)

`scripts/anchor_profile.py` (stdlib) calcula la distribución de anchors (marca, URL, genérico, exacto, parcial, natural) y la concentración por dominio desde el CSV de backlinks. Rangos de referencia: marca 30 a 50%, URL 15 a 25%, genérico 10 a 20%, exacto 3 a 10%, parcial 5 a 15%. Banderas: exacto sobre 15%, parcial sobre 25%, marca bajo 15%, un dominio con más del 10% de los enlaces. Concuerda con el criterio de Vero: anchor limpio y natural, sin sobreoptimizar.

## Señales extra de riesgo (revisión manual)

Alto riesgo: dominios con miles de enlaces salientes por página, enlaces de sitios hackeados (farmacia, casino), enlaces sitewide de pie de página desde sitios sin relación, anchors exactos desde 5 o más dominios no relacionados, redes de blogs privadas. Riesgo medio: nichos sin relación, enlaces recíprocos masivos, páginas de contenido muy delgado, más de 50 enlaces desde un mismo dominio. Monitorear: directorios genéricos, marcadores sociales, perfiles de foros, comentarios sin contexto editorial.

Se solapa con la rúbrica de 4 categorías de esta skill, que sigue mandando.

## Cuándo desautorizar (criterio de claude-seo, más conservador)

Sí: penalización manual, ataque de SEO negativo evidente, redes o granjas identificadas. No: enlaces de baja calidad que Google probablemente ignora, enlaces nofollow, pocos enlaces spam (menos de 2% del perfil). **Diferencia con esta skill:** la regla actual incluye nofollow de dominios tóxicos en el disavow; claude-seo lo desaconseja. Si dudas, documenta y consulta a Vero antes de subir el archivo. Google recomienda usar el disavow solo ante riesgo real.

## Puntuación de salud (opcional)

claude-seo calcula una nota 0 a 100 ponderando dominios referentes, calidad, anclas, toxicidad, velocidad, follow/nofollow y geografía, y se niega a dar nota si hay menos de 4 factores con datos. Regla adoptada aquí: **sin datos suficientes no hay nota, hay `pendiente de dato`**.

## Fuentes de datos gratuitas

Bing Webmaster Tools (solo tu sitio verificado), Moz API gratuita (cupo mensual), grafo web de Common Crawl (solo dominio) y verificación de enlaces conocidos (`link-building-y-outreach/scripts/verificar_enlaces.py`). Cobertura menor que Ahrefs o Semrush; indica siempre la fuente y su nivel de confianza.

## Banderas de velocidad

Picos de nuevos enlaces (posible ataque), pérdida de más de la mitad de enlaces en un mes (revisar acciones manuales en GSC) o ausencia de enlaces nuevos por 3 meses. Requieren datos históricos (Ahrefs); con fuentes gratuitas solo hay foto puntual.
