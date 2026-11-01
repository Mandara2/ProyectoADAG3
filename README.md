# Aceleración de una cadena de etapas bajo presupuesto

Proyecto semestral de **Análisis y Diseño de Algoritmos (2026-B)**, Universidad de Caldas, Grupo 3.

Dada una cadena de etapas en serie, el programa elige cuáles acelerar, sin pasarse de un presupuesto, para que la cadena termine lo antes posible. Lo resuelve de forma exacta con programación dinámica y entrega, por cada caso, el resultado, el tiempo y una traza de las decisiones.

## Contenido

- [El problema](#el-problema)
- [El algoritmo](#el-algoritmo)
- [Instalación](#instalación)
- [Uso](#uso)
- [Formato de entrada](#formato-de-entrada)
- [Formato de salida](#formato-de-salida)
- [Pruebas](#pruebas)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Limitaciones](#limitaciones)

## El problema

Una cadena tiene $n$ etapas en serie. Cada etapa $i$ dura $t_i$ y se puede acelerar pagando $c_i$, lo que le quita $d_i$ unidades de tiempo, con $0 \le d_i \le t_i$. Hay un presupuesto total $B$, entero.

Se busca el conjunto de etapas aceleradas $A$ que minimiza la duración total:

$$\min_{A} \; \sum_{i=1}^{n} t_i - \sum_{i \in A} d_i \qquad \text{sujeto a} \qquad \sum_{i \in A} c_i \le B$$

Como $\sum t_i$ es fijo, equivale a maximizar $\sum_{i \in A} d_i$. Es una mochila 0/1 donde el costo es el peso y la reducción es el valor.

**Alcance:** este repositorio cubre solo este problema. La cobertura mínima de auditoría del Subproyecto 3 queda por fuera, por indicación de la profesora.

## El algoritmo

$DP[i][b]$ es la mayor reducción posible usando las primeras $i$ etapas y gastando como máximo $b$:

$$
DP[i][b] =
\begin{cases}
\max\big(DP[i-1][b],\; DP[i-1][b-c_i] + d_i\big) & \text{si } c_i \le b \\
DP[i-1][b] & \text{si } c_i > b
\end{cases}
\qquad DP[0][b] = 0
$$

La respuesta es $DP[n][B]$. Para saber qué etapas se aceleraron se recorre la tabla hacia atrás: si $DP[i][b] \ne DP[i-1][b]$, la etapa $i$ se acelera y $b$ baja en $c_i$.

| Paso | Costo |
| --- | --- |
| Llenar la tabla de $(n+1)(B+1)$ casillas | $O(n \cdot B)$ |
| Reconstruir las etapas aceleradas | $O(n)$ |

El costo es **pseudo-polinomial**: depende del valor de $B$, así que es exponencial en la cantidad de bits con que se escribe $B$.

## Instalación

Requiere Python 3.10 o superior. No usa librerías externas.

```bash
git clone <url-de-este-repositorio>
cd <carpeta-del-repositorio>
```

## Uso

Correr los casos de ejemplo:

```bash
python src/main.py pruebas/casos
```

Correr los casos de la profesora, guardados en `casos/`:

```bash
python src/main.py casos
```

Por defecto las salidas van a `resultados/`. Se puede indicar otra carpeta como segundo argumento:

```bash
python src/main.py casos otra_carpeta
```

Salida en pantalla con los casos de ejemplo (el tiempo varía según el equipo):

```text
ejemplo_almuerzo: acelerar [2, 3], costo 5/5, duración 28 -> 6, 0.006 ms
ejemplo_tres_etapas: acelerar [1, 3], costo 9/10, duración 22 -> 15, 0.006 ms
```

## Formato de entrada

Un archivo `.json` por caso:

```json
{
  "id": "ejemplo_tres_etapas",
  "B": 10,
  "etapas": [
    { "t": 8, "c": 4, "d": 3 },
    { "t": 5, "c": 3, "d": 2 },
    { "t": 9, "c": 5, "d": 4 }
  ]
}
```

| Campo | Significado |
| --- | --- |
| `id` | Nombre del caso; también nombra el archivo de salida |
| `B` | Presupuesto total |
| `t` | Duración normal de la etapa |
| `c` | Costo de acelerarla |
| `d` | Tiempo que se reduce al acelerarla |

Todos los números son enteros mayores o iguales a 0 y debe cumplirse `d <= t`. Un caso inválido se reporta en pantalla y no detiene los demás.

## Formato de salida

Por cada caso se crea `resultados/<id>.json`, y además `resultados/resumen.json` con una fila por caso.

| Campo | Significado |
| --- | --- |
| `etapas_aceleradas` | Etapas elegidas, numeradas desde 1 |
| `costo_usado` | Suma de los costos de esas etapas |
| `reduccion` | Tiempo total que se quita |
| `duracion_original`, `duracion_final` | Duración antes y después de acelerar |
| `tiempo_ms` | Promedio de 5 ejecuciones, en milisegundos |
| `traza.reconstruccion` | Una fila por etapa con `b`, `DP[i][b]`, `DP[i-1][b]`, la decisión y el presupuesto restante |
| `traza.tabla` | Tabla completa, solo si tiene menos de 500 casillas |

## Pruebas

```bash
python -m unittest discover -s pruebas
```

Las 10 pruebas cubren:

- Los ejemplos con respuesta conocida.
- Los casos borde: presupuesto 0, sin etapas, costo mayor que el presupuesto y costo 0.
- La validación de casos inválidos.
- 300 casos aleatorios con semilla fija, comparados contra fuerza bruta.

## Estructura del repositorio

```text
├── src/
│   ├── lectura.py       lee y valida los casos
│   ├── aceleracion.py   tabla DP, reconstrucción y traza
│   └── main.py          corre los casos, mide el tiempo y guarda las salidas
├── pruebas/
│   ├── test_aceleracion.py
│   └── casos/           casos de ejemplo con respuesta conocida
├── casos/               casos de la profesora, sin modificar
├── resultados/          salidas del programa
└── docs/
    └── MANUAL_TECNICO.md
```

Solo `src/lectura.py` conoce el formato de entrada. Si los casos llegan en otro formato, ese es el único archivo que cambia.

## Limitaciones

- Con un $B$ muy grande la tabla no cabe en memoria o tarda demasiado.
- Solo acepta valores enteros.
- Cuando hay varias soluciones óptimas, devuelve una sola.

Más detalles en el [manual técnico](docs/MANUAL_TECNICO.md).
