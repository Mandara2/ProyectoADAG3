# Manual técnico

**Proyecto:** aceleración de una cadena de etapas bajo presupuesto (Subproyecto 3, primer problema).
**Curso:** Análisis y Diseño de Algoritmos 2026-B, Universidad de Caldas.
**Grupo 3:** Rafael Medina e Isabela Guerrero.

Este manual explica cómo está construida la solución, cómo se ejecuta, qué formatos usa y cuáles son sus límites.

## 1. Qué resuelve

Una cadena tiene `n` etapas en serie. La etapa `i` dura `t_i`; acelerarla cuesta `c_i` y le quita `d_i` unidades de tiempo (`0 <= d_i <= t_i`). Con un presupuesto entero `B`, el programa elige qué etapas acelerar para que la cadena dure lo menos posible.

Como la duración sin acelerar, `Σ t_i`, es fija, el programa maximiza la reducción `Σ d_i` de las etapas elegidas, con la condición de que `Σ c_i <= B`. Es una mochila 0/1: el costo hace de peso y la reducción hace de valor.

## 2. Requisitos e instalación

- Python 3.10 o superior.
- No usa librerías externas, así que no hay que instalar dependencias.

```bash
git clone https://github.com/Mandara2/ProyectoADAG3.git
cd ProyectoADAG3
```

Todos los comandos de este manual se ejecutan desde la raíz del repositorio.

## 3. Ejecución

| Qué se quiere | Comando |
| --- | --- |
| Correr un solo caso | `python src/main.py ruta/al/caso.json` |
| Correr todos los casos de una carpeta | `python src/main.py pruebas/casos` |
| Elegir dónde guardar las salidas | `python src/main.py pruebas/casos otra_carpeta` |
| Correr las pruebas automáticas | `python -m unittest discover -s pruebas` |
| Generar un caso aleatorio | `python src/generar_casos.py <n> <semilla> [carpeta]` |

Por defecto las salidas se guardan en `resultados/`. Por cada caso, el programa imprime una línea en pantalla:

```text
ejemplo_tres_etapas: acelerar [1, 3], costo 9/10, duración 22 -> 15, 0.007 ms
```

Si un caso es inválido, el programa lo reporta y sigue con los demás:

```text
roto.json: INVÁLIDO, en la etapa 1 no se cumple d <= t (3 > 2)
```

## 4. Formato de entrada

Cada caso es un archivo `.json`:

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

| Campo | Tipo | Significado |
| --- | --- | --- |
| `id` | texto | Nombre del caso. También es el nombre del archivo de salida. |
| `B` | entero `>= 0` | Presupuesto total. |
| `etapas` | lista | Una entrada por etapa, en el orden de la cadena. |
| `t` | entero `>= 0` | Duración normal de la etapa. |
| `c` | entero `>= 0` | Costo de acelerarla. |
| `d` | entero, `0 <= d <= t` | Tiempo que se reduce si se acelera. |
| `esperado` | opcional | Respuesta conocida. Solo la usan las pruebas automáticas; el programa la ignora. |

Las etapas se numeran desde 1 según su posición en la lista.

Un caso se rechaza si:
- No es JSON válido.
- Le falta `id`, `B` o `etapas`.
- `etapas` no es una lista, o una etapa no tiene `t`, `c` y `d`.
- Algún número no es un entero mayor o igual a 0.
- En alguna etapa `d > t`.

## 5. Formato de salida

Por cada caso se crea `resultados/<id>.json`:

| Campo | Significado |
| --- | --- |
| `id`, `n` | Nombre del caso y número de etapas |
| `tiempo_ms` | Tiempo promedio de 5 ejecuciones del algoritmo, en milisegundos. No incluye la lectura del archivo. |
| `etapas_aceleradas` | Etapas elegidas, en orden |
| `costo_usado`, `presupuesto` | Lo que se gastó y lo que había |
| `reduccion` | Tiempo total quitado: `DP[n][B]` |
| `duracion_original`, `duracion_final` | Duración antes y después de acelerar |
| `traza.casillas_tabla` | Tamaño de la tabla: `(n+1)(B+1)` |
| `traza.reconstruccion` | Una fila por etapa, de la última a la primera: `etapa`, `b`, `DP[i][b]`, `DP[i-1][b]`, `decision` y `presupuesto_restante` |
| `traza.tabla` | La tabla DP completa. Solo aparece si tiene menos de 500 casillas. |

Además se crea `resultados/resumen.json`, con una fila por caso.

## 6. Estructura del código

```text
src/
├── lectura.py        lee y valida los casos
├── aceleracion.py    algoritmo: tabla, reconstrucción y traza
├── main.py           corre los casos, mide el tiempo y escribe las salidas
└── generar_casos.py  crea casos aleatorios reproducibles
pruebas/
├── test_aceleracion.py
└── casos/            casos propios, con respuesta esperada cuando n <= 16
```

### 6.1 `lectura.py`

Es el único archivo que conoce el formato de entrada. Si los casos llegan en otro formato, solo cambia este archivo.

| Función | Qué hace |
| --- | --- |
| `validar_caso(datos)` | Revisa un caso ya cargado y devuelve `(id, B, etapas)`. Lanza `CasoInvalido` con un mensaje claro si algo falla. |
| `leer_caso(ruta)` | Abre el archivo, lo convierte de JSON y llama a `validar_caso`. |
| `listar_casos(ruta)` | Si `ruta` es un archivo, devuelve solo ese; si es una carpeta, devuelve sus `.json` en orden alfabético. |

### 6.2 `aceleracion.py`

| Función | Qué hace | Costo |
| --- | --- | --- |
| `llenar_tabla(etapas, B)` | Construye la tabla DP de `(n+1) x (B+1)` | `O(n·B)` |
| `reconstruir(dp, etapas, B)` | Recorre la tabla hacia atrás y decide qué etapas se aceleraron | `O(n)` |
| `resolver(etapas, B)` | Llama a las dos anteriores y arma el resultado con su traza | `O(n·B)` |

### 6.3 `main.py`

1. Recibe un archivo o una carpeta.
2. Para cada caso: lo lee con `leer_caso`, ejecuta `resolver` 5 veces midiendo con `time.perf_counter()` y promedia el tiempo.
3. Escribe `resultados/<id>.json` e imprime la línea resumen.
4. Al final escribe `resultados/resumen.json`.

### 6.4 `generar_casos.py`

Crea un caso aleatorio a partir de `n` y una semilla. La misma semilla siempre produce el mismo caso. Cada etapa tiene `t` entre 1 y 20, `d` entre 0 y `t` y `c` entre 1 y 15. El presupuesto es la mitad de la suma de los costos, para que no todas las etapas quepan.

## 7. El algoritmo, paso a paso

`DP[i][b]` es la mayor reducción que se puede lograr usando solo las primeras `i` etapas y gastando como máximo `b`.

- `DP[0][b] = 0`: sin etapas no hay reducción.
- Si `c_i > b`, la etapa `i` no cabe: `DP[i][b] = DP[i-1][b]`.
- Si `c_i <= b`, se toma la mejor opción entre no acelerarla, `DP[i-1][b]`, y acelerarla, `DP[i-1][b - c_i] + d_i`.

La respuesta es `DP[n][B]`.

**Reconstrucción.** Se empieza en `i = n`, `b = B`. Si `DP[i][b]` es distinto de `DP[i-1][b]`, la etapa `i` se usó: se acelera y `b` baja en `c_i`. Si son iguales, no se aceleró. Luego se pasa a `i - 1`.

**Ejemplo** (`ejemplo_tres_etapas`, con `B = 10` y etapas `(t, c, d)`: `(8, 4, 3)`, `(5, 3, 2)` y `(9, 5, 4)`):

| Etapa | b | DP[i][b] | DP[i-1][b] | Decisión | Presupuesto restante |
| --- | --- | --- | --- | --- | --- |
| 3 | 10 | 7 | 5 | acelerar | 5 |
| 2 | 5 | 3 | 3 | no acelerar | 5 |
| 1 | 5 | 3 | 0 | acelerar | 1 |

Se aceleran las etapas 1 y 3, con costo 9. La reducción es 7 y la duración pasa de 22 a 15.

## 8. Casos de prueba propios

Están en `pruebas/casos/`. La respuesta esperada se calculó por fuerza bruta, probando todos los subconjuntos, sin usar la DP.

| Caso | Qué prueba | Reducción esperada |
| --- | --- | --- |
| `ejemplo_tres_etapas` | Caso básico con traza conocida | 7 |
| `ejemplo_almuerzo` | El presupuesto se usa completo | 22 |
| `voraz_por_razon_falla` | Elegir por mejor razón `d/c` daría 160; el óptimo es 220 | 220 |
| `borde_presupuesto_cero` | `B = 0` | 0 |
| `borde_costo_cero` | Una etapa con costo 0 se acelera sin gastar | 2 |
| `borde_nada_cabe` | Ninguna etapa cabe en el presupuesto | 0 |
| `borde_todo_cabe` | Todas caben | 11 |
| `borde_sin_reduccion` | Una etapa con `d = 0` | 4 |
| `aleatorio_n15_s7` | Caso generado con 15 etapas | 87 |
| `aleatorio_n200_s1` | Caso grande: 200 etapas, `B = 824` | sin respuesta esperada; mide tiempo |

## 9. Pruebas automáticas

`python -m unittest discover -s pruebas` corre 14 pruebas:

- Los ejemplos con resultado y traza conocidos.
- Los casos borde.
- Todos los casos de `pruebas/casos`, comparados con su campo `esperado`.
- 300 casos aleatorios con semilla fija, comparados contra fuerza bruta.
- La validación: `d > t`, presupuesto no entero, `etapas` que no es lista y JSON mal escrito.

## 10. Limitaciones

- **Pseudo-polinomial:** el tiempo y la memoria crecen con el valor de `B`. Con un `B` de millones, la tabla tiene millones de casillas por etapa y puede no caber en memoria.
- Solo acepta valores enteros. Un `B` con decimales se rechaza.
- Si hay varias soluciones óptimas, devuelve una sola. Por cómo funciona la reconstrucción, cuando hay empate prefiere no acelerar la etapa de número mayor.
- La tabla completa solo se guarda en la traza si tiene menos de 500 casillas, para que los archivos de salida no sean enormes.
- No incluye la parte de auditoría del Subproyecto 3, por indicación del curso.
