"""Corre uno o varios casos y guarda resultado, tiempo y traza.

Uso: python src/main.py <archivo.json | carpeta> [carpeta_de_salida] [--detalle]

Con un solo archivo se muestra el detalle completo del caso en cuatro bloques:
datos, programación dinámica (tabla y reconstrucción), comprobación por
fuerza bruta y veredicto. Con una carpeta solo se muestra una línea por caso,
salvo que se agregue --detalle.
"""

import json
import sys
import time
from pathlib import Path

from aceleracion import resolver
from comprobar import comprobar, escribir_datos, veredicto
from lectura import CasoInvalido, leer_caso, listar_casos
from tabla import formatear

# Un caso pequeño tarda microsegundos: se repite y se promedia el tiempo.
REPETICIONES = 5
ANCHO = 72


def mostrar_detalle(id_caso, presupuesto, etapas, resultado, salida):
    """Imprime el caso en cuatro bloques y guarda el registro de la comprobación."""
    registro = [f"=== Comprobación por fuerza bruta: {id_caso} ==="]

    def bloque(numero, titulo):
        print("-" * ANCHO)
        print(f"[{numero}] {titulo}")
        print("-" * ANCHO)

    def escribir(texto):
        print(texto)
        registro.append(texto)

    print("=" * ANCHO)
    print(f"CASO: {id_caso}")
    print("=" * ANCHO)

    bloque(1, "DATOS DEL CASO")
    escribir_datos(presupuesto, etapas, escribir)

    bloque(2, "PROGRAMACIÓN DINÁMICA: la solución")
    print("\n".join(formatear(etapas, resultado)))

    bloque(3, "COMPROBACIÓN POR FUERZA BRUTA: independiente de la DP")
    registro.append("")
    fuerza = comprobar(etapas, presupuesto, escribir)

    bloque(4, "VEREDICTO")
    registro.append("")
    coincide = veredicto(resultado, fuerza, escribir)
    print("=" * ANCHO)
    print()

    carpeta = salida / "comprobacion"
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / f"{id_caso}.log").write_text("\n".join(registro) + "\n", encoding="utf-8")
    return coincide


def medir(etapas, presupuesto):
    """Devuelve el resultado y el tiempo promedio en milisegundos."""
    inicio = time.perf_counter()
    for _ in range(REPETICIONES):
        resultado = resolver(etapas, presupuesto)
    total = time.perf_counter() - inicio
    return resultado, total / REPETICIONES * 1000


def correr_caso(ruta, salida, detalle=False):
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
    fila = {
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
    if detalle:
        print()
        fila["coincide_con_fuerza_bruta"] = mostrar_detalle(id_caso, presupuesto, etapas, resultado, salida)
    return fila


def main():
    opciones = {"--detalle", "--tabla"}
    argumentos = [a for a in sys.argv[1:] if a not in opciones]
    if not argumentos:
        print("Uso: python src/main.py <archivo.json | carpeta> [carpeta_de_salida] [--detalle]")
        return 1

    entrada = Path(argumentos[0])
    salida = Path(argumentos[1]) if len(argumentos) > 1 else Path("resultados")
    salida.mkdir(parents=True, exist_ok=True)

    casos = listar_casos(entrada)
    if not casos:
        print(f"No se encontraron casos .json en {entrada}")
        return 1

    detalle = entrada.is_file() or any(a in opciones for a in sys.argv[1:])
    resumen = [correr_caso(ruta, salida, detalle) for ruta in casos]
    with open(salida / "resumen.json", "w", encoding="utf-8") as archivo:
        json.dump(resumen, archivo, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
