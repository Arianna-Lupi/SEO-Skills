# Método de proyección y supuestos

## Qué es real y qué es supuesto

| Elemento | Origen |
|---|---|
| Línea base de clics e impresiones | **Real**: promedio de los últimos 3 meses completos de Search Console (desestacionalizado si hay 12 meses o más) |
| CTR actual de cada página | **Real**: clics / impresiones de esa página en Search Console |
| Curva de CTR por posición | **Real** si la web tiene muestra (por defecto 500 impresiones y 3 consultas por posición); si no, **supuesto del usuario** (`--curva-generica`), rotulado |
| Estacionalidad | **Real pero frágil**: índice por mes calendario sobre la tendencia lineal de 12 meses; con un año de historial es un supuesto a revisar |
| Cumplimiento del plan, posición objetivo, meses de maduración | **Supuestos editables** de cada escenario |
| Volumen de páginas nuevas | **Aportado por el usuario** desde su herramienta; sin él, la página no suma (`pendiente de dato`) |

## Escenarios por defecto (SUPUESTOS EDITABLES, no son datos)

| | Cumplimiento | Posición objetivo | Meses de maduración |
|---|---|---|---|
| Conservador | 0,6 | 10 | 6 |
| Base | 0,8 | 5 | 4 |
| Optimista | 1,0 | 3 | 3 |

Se cambian con `--supuestos`:

```json
{"conservador": {"cumplimiento": 0.5, "posicion_objetivo": 12, "meses_maduracion": 8}, "base": {"meses_maduracion": 5}}
```

## Fórmulas

- **Madurez(t)** = min(1, t / meses_maduración), con t = meses desde la publicación (0 en el mes de publicación, 0 antes).
- **Página existente (acción Actualizar):** clics del mes = impresiones del mes de la página × max(0, CTR(posición objetivo) − CTR actual real) × cumplimiento × madurez(t). Las impresiones por mes salen del export por página dividido entre los meses que cubre (`--meses-paginas`).
- **Página nueva (acción Crear):** clics del mes = volumen aportado × CTR(posición objetivo) × cumplimiento × madurez(t).
- **Total proyectado del mes** = línea base × índice de estacionalidad + suma de incrementales.
- **CTR(posición)**: interpolación lineal entre las posiciones con muestra suficiente.
- **Rango por mes**: mínimo = escenario conservador, base = escenario base, máximo = escenario optimista.

## Limitaciones que debes decir al cliente

- Las impresiones se asumen constantes: no se modelan cambios de demanda, de algoritmo ni de competencia.
- No hay canibalización entre páginas nuevas y existentes.
- El tiempo hasta rankear es un supuesto (meses de maduración). Si el sitio tiene historial de páginas nuevas, úsalo para calibrar el supuesto a mano.
- Una proyección con menos de 12 meses no captura estacionalidad.
- Posiciones por debajo de 10 no están en la curva: las páginas fuera de la primera página dependen de la interpolación hacia el extremo.

## Seguimiento

`seguimiento` compara cada mes real con el rango. Estados: dentro del rango, por debajo del conservador, por encima del optimista, sin dato real todavía. Cuando está por debajo, revisa primero el cumplimiento del plan, luego impresiones contra CTR (Semana 12) y recién después factores externos.
