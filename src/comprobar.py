"""Comprobación por fuerza bruta: revisa todas las combinaciones de etapas.

Uso: python src/comprobar.py <archivo.json | carpeta> [carpeta_de_salida]

Para cada caso prueba los 2^n subconjuntos de etapas, deja un registro de cada
uno (costo, si cabe, reducción, duración y si mejora lo anterior) y al final
compara el óptimo encontrado con el de la programación dinámica. Es
independiente de la DP, así que sirve para comprobar que la DP no se equivoca.

El registro se imprime en pantalla y se guarda en
<carpeta_de_salida>/<id>.log (por defecto resultados/comprobacion/).
"""

import sys
from itertools import combinations
from pathlib import Path

from aceleracion import resolver
from lectura import CasoInvalido, leer_caso, listar_casos

# Con más etapas, 2^n combinaciones ya son demasiadas para probarlas todas.
MAX_ETAPAS = 20
# Hasta este número de combinaciones se escribe una línea por cada una; con
# más, solo se escriben las que mejoran el mejor resultado hasta el momento.
MAX_LINEAS_DETALLE = 1024


def _conjunto(grupo):
    return "{" + ", ".join(map(str, grupo)) + "}" if grupo else "{}"


def fuerza_bruta(etapas, presupuesto, escribir):
    """Prueba todos los subconjuntos en orden de tamaño y registra cada uno.

    Devuelve (mejor_reduccion, lista_de_conjuntos_optimos).
    """
    n = len(etapas)
    total = 2 ** n
    detalle = total <= MAX_LINEAS_DETALLE
    duracion_original = sum(etapa["t"] for etapa in etapas)

    escribir(f"Se revisan 2^{n} = {total} combinaciones.")
    if not detalle:
        escribir(f"Son más de {MAX_LINEAS_DETALLE}: solo se muestran las que mejoran el resultado.")
    escribir("")
    escribir(f"{'#':>5}  {'Etapas aceleradas':<22} {'Costo':>6}  {'Cabe':<4} {'Reducción':>9} {'Duración':>8}  Nota")

    mejor, optimos, numero = -1, [], 0
    for tam in range(n + 1):
        for grupo in combinations(range(1, n + 1), tam):
            numero += 1
            costo = sum(etapas[i - 1]["c"] for i in grupo)
            cabe = costo <= presupuesto
            if not cabe:
                nota = f"no cabe: {costo} > {presupuesto}"
                if detalle:
                    escribir(f"{numero:>5}  {_conjunto(grupo):<22} {costo:>6}  {'no':<4} {'-':>9} {'-':>8}  {nota}")
                continue

            reduccion = sum(etapas[i - 1]["d"] for i in grupo)
            if reduccion > mejor:
                nota = "nuevo mejor"
                mejor, optimos = reduccion, [list(grupo)]
            elif reduccion == mejor:
                nota = "empata con el mejor"
                optimos.append(list(grupo))
            else:
                nota = ""
            if detalle or nota:
                duracion = duracion_original - reduccion
                escribir(f"{numero:>5}  {_conjunto(grupo):<22} {costo:>6}  {'sí':<4} {reduccion:>9} {duracion:>8}  {nota}")

    return mejor, optimos


def escribir_datos(presupuesto, etapas, escribir):
    """Escribe los datos del caso tal como se leyeron."""
    duracion_original = sum(etapa["t"] for etapa in etapas)
    escribir(f"n = {len(etapas)} etapas, presupuesto B = {presupuesto}, duración sin acelerar = {duracion_original}")
    for i, etapa in enumerate(etapas, start=1):
        escribir(f"  etapa {i}: t = {etapa['t']}, c = {etapa['c']}, d = {etapa['d']}")


def comprobar(etapas, presupuesto, escribir):
    """Busca el óptimo por fuerza bruta y lo registra.

    Devuelve (mejor_reduccion, optimos), o None si el caso es demasiado
    grande para probar todas las combinaciones.
    """
    n = len(etapas)
    if n > MAX_ETAPAS:
        escribir(f"No se comprueba: con n = {n} habría 2^{n} combinaciones (el límite es n = {MAX_ETAPAS}).")
        return None

    duracion_original = sum(etapa["t"] for etapa in etapas)
    mejor, optimos = fuerza_bruta(etapas, presupuesto, escribir)
    escribir("")
    escribir(f"Fuerza bruta: reducción máxima {mejor}, duración {duracion_original} -> {duracion_original - mejor}.")
    escribir(f"Soluciones óptimas ({len(optimos)}): " + ", ".join(_conjunto(g) for g in optimos))
    return mejor, optimos


def veredicto(dp, fuerza, escribir):
    """Compara la DP con la fuerza bruta. Devuelve True, False o None."""
    escribir(f"Programación dinámica: acelera {_conjunto(dp['etapas_aceleradas'])}, "
             f"reducción {dp['reduccion']}, costo {dp['costo_usado']}.")
    if fuerza is None:
        escribir("Resultado: SIN COMPROBAR. El caso es demasiado grande para la fuerza bruta.")
        return None
    mejor, optimos = fuerza
    coincide = dp["reduccion"] == mejor and dp["etapas_aceleradas"] in optimos
    if coincide:
        escribir("Resultado: COINCIDE. La DP encontró una de las soluciones óptimas.")
    else:
        escribir("Resultado: NO COINCIDE. Revisar la DP.")
    return coincide


def comprobar_caso(id_caso, presupuesto, etapas, escribir):
    """Comprueba un caso y devuelve True si la DP coincide con la fuerza bruta."""
    escribir(f"=== Comprobación por fuerza bruta: {id_caso} ===")
    escribir_datos(presupuesto, etapas, escribir)
    escribir("")
    fuerza = comprobar(etapas, presupuesto, escribir)
    if fuerza is None:
        return None
    return veredicto(resolver(etapas, presupuesto), fuerza, escribir)


def main():
    if len(sys.argv) < 2:
        print("Uso: python src/comprobar.py <archivo.json | carpeta> [carpeta_de_salida]")
        return 1

    entrada = Path(sys.argv[1])
    salida = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("resultados/comprobacion")
    salida.mkdir(parents=True, exist_ok=True)

    casos = listar_casos(entrada)
    if not casos:
        print(f"No se encontraron casos .json en {entrada}")
        return 1

    fallos = 0
    for ruta in casos:
        try:
            id_caso, presupuesto, etapas = leer_caso(ruta)
        except CasoInvalido as error:
            print(f"{ruta.name}: INVÁLIDO, {error}\n")
            continue

        lineas = []

        def escribir(texto):
            print(texto)
            lineas.append(texto)

        if comprobar_caso(id_caso, presupuesto, etapas, escribir) is False:
            fallos += 1
        (salida / f"{id_caso}.log").write_text("\n".join(lineas) + "\n", encoding="utf-8")
        print()

    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
