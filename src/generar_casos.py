"""Genera casos sintéticos reproducibles (misma semilla, mismo caso).

Uso: python src/generar_casos.py <n> <semilla> [carpeta_de_salida]

Cada etapa tiene t entre 1 y 20, d entre 0 y t, y c entre 1 y 15.
El presupuesto es la mitad de la suma de los costos, para que no todo quepa.
"""

import json
import random
import sys
from pathlib import Path


def generar(n, semilla):
    rng = random.Random(semilla)
    etapas = []
    for _ in range(n):
        t = rng.randint(1, 20)
        etapas.append({"t": t, "c": rng.randint(1, 15), "d": rng.randint(0, t)})
    presupuesto = sum(etapa["c"] for etapa in etapas) // 2
    return {"id": f"aleatorio_n{n}_s{semilla}", "B": presupuesto, "etapas": etapas}


def main():
    if len(sys.argv) < 3:
        print("Uso: python src/generar_casos.py <n> <semilla> [carpeta_de_salida]")
        return 1

    n, semilla = int(sys.argv[1]), int(sys.argv[2])
    salida = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("pruebas/casos")
    salida.mkdir(parents=True, exist_ok=True)

    caso = generar(n, semilla)
    ruta = salida / f"{caso['id']}.json"
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(caso, archivo, ensure_ascii=False, indent=2)
    print(f"Caso guardado en {ruta}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
