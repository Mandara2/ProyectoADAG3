# Manual técnico (borrador)

Falta completarlo con la versión final del código y el formato real de los casos.

## Algoritmo

`DP[i][b]` es la máxima reducción de tiempo usando las primeras `i` etapas y gastando como máximo `b`.

- `DP[0][b] = 0`
- Si `c_i > b`: `DP[i][b] = DP[i-1][b]`
- Si `c_i <= b`: `DP[i][b] = max(DP[i-1][b], DP[i-1][b-c_i] + d_i)`

La respuesta es `DP[n][B]`. Las etapas aceleradas se obtienen recorriendo la tabla hacia atrás: si `DP[i][b]` es distinto de `DP[i-1][b]`, la etapa `i` se acelera y `b` baja en `c_i`.

Costo: `O(n·B)` para llenar la tabla y `O(n)` para reconstruir.

## Estructura del código

| Archivo | Función |
| --- | --- |
| `src/lectura.py` | Lee y valida los casos. Es el único archivo que conoce el formato. |
| `src/aceleracion.py` | Llena la tabla, reconstruye la solución y arma la traza. |
| `src/main.py` | Recorre los casos, mide el tiempo y escribe las salidas. |

## Formatos

**Entrada:** un archivo JSON por caso, con `id`, `B` y `etapas` (cada una con `t`, `c` y `d`).

**Salida:** un archivo JSON por caso con las etapas aceleradas, el costo usado, la reducción, la duración original y final, el tiempo en milisegundos y la traza. La traza trae una fila por etapa con `i`, `b`, `DP[i][b]`, `DP[i-1][b]`, la decisión y el presupuesto restante. La tabla completa solo se incluye si tiene menos de 500 casillas.

## Ejecución

Ver `README.md`.

## Limitaciones

- La DP es pseudo-polinomial: con `B` muy grande la tabla no cabe en memoria o tarda demasiado.
- Solo acepta costos y presupuesto enteros.
- El tiempo reportado es el promedio de 5 ejecuciones.
- No incluye la parte de auditoría, por indicación de la profesora.
