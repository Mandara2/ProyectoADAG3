"""Lectura y validación de casos.

Es el único archivo que conoce el formato de entrada. Si la profesora entrega
los casos en otro formato, solo se cambia este archivo.
"""

import json
from pathlib import Path


class CasoInvalido(Exception):
    """El caso no cumple las condiciones del enunciado."""


def _entero_no_negativo(valor, nombre):
    # bool es subclase de int en Python, por eso se excluye aparte.
    if not isinstance(valor, int) or isinstance(valor, bool) or valor < 0:
        raise CasoInvalido(f"{nombre} debe ser un entero >= 0 y es {valor!r}")
    return valor


def validar_caso(datos):
    """Revisa un caso ya cargado y devuelve (id, B, etapas)."""
    for campo in ("id", "B", "etapas"):
        if campo not in datos:
            raise CasoInvalido(f"falta el campo '{campo}'")

    presupuesto = _entero_no_negativo(datos["B"], "B")

    etapas = []
    for i, etapa in enumerate(datos["etapas"], start=1):
        for campo in ("t", "c", "d"):
            if campo not in etapa:
                raise CasoInvalido(f"a la etapa {i} le falta '{campo}'")
        t = _entero_no_negativo(etapa["t"], f"t de la etapa {i}")
        c = _entero_no_negativo(etapa["c"], f"c de la etapa {i}")
        d = _entero_no_negativo(etapa["d"], f"d de la etapa {i}")
        if d > t:
            raise CasoInvalido(f"en la etapa {i} no se cumple d <= t ({d} > {t})")
        etapas.append({"t": t, "c": c, "d": d})

    return datos["id"], presupuesto, etapas


def leer_caso(ruta):
    """Lee un caso desde un archivo JSON."""
    with open(ruta, encoding="utf-8") as archivo:
        return validar_caso(json.load(archivo))


def listar_casos(carpeta):
    """Devuelve las rutas de los casos de la carpeta, en orden alfabético."""
    return sorted(Path(carpeta).glob("*.json"))
