# Proyecto ADAG 2026-B, Grupo 3: aceleración de la cadena bajo presupuesto

Solución base del primer problema del Subproyecto 3: elegir qué etapas acelerar, sin pasarse del presupuesto `B`, para que la cadena dure lo menos posible. Se resuelve con programación dinámica en `O(n·B)`.

## Requisitos

Python 3.10 o superior. No usa librerías externas.

## Cómo ejecutar

Desde esta carpeta, para correr los casos de ejemplo:

```bash
python src/main.py pruebas/casos
```

Para correr los casos de la profesora, guardados en `casos/`:

```bash
python src/main.py casos
```

Se crea un archivo por caso en `resultados/` con el resultado, el tiempo y la traza, y además `resultados/resumen.json`.

Para correr las pruebas:

```bash
python -m unittest discover -s pruebas
```

## Formato de un caso

```json
{
  "id": "caso_01",
  "B": 10,
  "etapas": [ { "t": 8, "c": 4, "d": 3 } ]
}
```

`t` es la duración, `c` el costo de acelerar y `d` el tiempo que se reduce. Todos son enteros `>= 0` y debe cumplirse `d <= t`.

## Estructura

- `src/lectura.py`: lee y valida los casos.
- `src/aceleracion.py`: tabla DP, reconstrucción y traza.
- `src/main.py`: corre los casos, mide el tiempo y guarda las salidas.
- `pruebas/`: pruebas y casos de ejemplo con respuesta conocida.
- `casos/`: casos de la profesora, sin modificar.
- `docs/MANUAL_TECNICO.md`: manual técnico.
