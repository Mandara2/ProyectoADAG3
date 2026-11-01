"""Corre todos los casos de una carpeta y guarda resultado, tiempo y traza.

Uso: python src/main.py casos/ [carpeta_de_salida]
"""

import json
import sys
import time
from pathlib import Path

from aceleracion import resolver
from lectura import CasoInvalido, leer_caso, listar_casos

# Un caso pequeño tarda microsegundos: se repite y se promedia el tiempo.
REPETICIONES = 5


def medir(etapas, presupuesto):
    """Devuelve el resultado y el tiempo promedio en milisegundos."""
    inicio = time.perf_counter()
    for _ in range(REPETICIONES):
        resultado = resolver(etapas, presupuesto)
    total = time.perf_counter() - inicio
    return resultado, total / REPETICIONES * 1000


def correr_caso(ruta, salida):
    """Procesa un caso y devuelve su fila para el resumen."""
    try:
        id_caso, presupuesto, etapas = leer_caso(ruta)
    except CasoInvalido as error:
        print(f"{ruta.name}: INVÁLIDO, {error}")
        return {"archivo": ruta.name, "estado": f"inválido: {error}"}

    resultado, tiempo_ms = medir(etapas, presupuesto)
    registro = {"id": id_caso, "n": len(etapas), "tiempo_ms": tiempo_ms, **resultado}

    with open(salida / f"{id_caso}.json", "w", encoding="utf-8") as archivo:
        json.dump(registro, archivo, ensure_ascii=False, indent=2)

    print(
        f"{id_caso}: acelerar {resultado['etapas_aceleradas']}, "
        f"costo {resultado['costo_usado']}/{presupuesto}, "
        f"duración {resultado['duracion_original']} -> {resultado['duracion_final']}, "
        f"{tiempo_ms:.3f} ms"
    )
    return {
        "archivo": ruta.name,
        "estado": "ok",
        "id": id_caso,
        "n": len(etapas),
        "B": presupuesto,
        "etapas_aceleradas": resultado["etapas_aceleradas"],
        "costo_usado": resultado["costo_usado"],
        "duracion_final": resultado["duracion_final"],
        "tiempo_ms": tiempo_ms,
    }


def main():
    if len(sys.argv) < 2:
        print("Uso: python src/main.py <carpeta_de_casos> [carpeta_de_salida]")
        return 1

    entrada = Path(sys.argv[1])
    salida = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("resultados")
    salida.mkdir(parents=True, exist_ok=True)

    casos = listar_casos(entrada)
    if not casos:
        print(f"No hay archivos .json en {entrada}")
        return 1

    resumen = [correr_caso(ruta, salida) for ruta in casos]
    with open(salida / "resumen.json", "w", encoding="utf-8") as archivo:
        json.dump(resumen, archivo, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
