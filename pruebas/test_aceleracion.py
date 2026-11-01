"""Pruebas de la Parte 1. Uso: python -m unittest discover -s pruebas"""

import random
import sys
import unittest
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from aceleracion import resolver
from lectura import CasoInvalido, validar_caso


def etapas(*ternas):
    return [{"t": t, "c": c, "d": d} for t, c, d in ternas]


def fuerza_bruta(lista, presupuesto):
    """Prueba los 2^n subconjuntos; solo sirve para comparar con n pequeño."""
    mejor = 0
    for tam in range(len(lista) + 1):
        for grupo in combinations(lista, tam):
            if sum(e["c"] for e in grupo) <= presupuesto:
                mejor = max(mejor, sum(e["d"] for e in grupo))
    return mejor


class EjemplosDeLaGuia(unittest.TestCase):
    def test_tres_etapas(self):
        r = resolver(etapas((8, 4, 3), (5, 3, 2), (9, 5, 4)), 10)
        self.assertEqual(r["etapas_aceleradas"], [1, 3])
        self.assertEqual(r["costo_usado"], 9)
        self.assertEqual(r["duracion_original"], 22)
        self.assertEqual(r["duracion_final"], 15)

    def test_traza_de_tres_etapas(self):
        r = resolver(etapas((8, 4, 3), (5, 3, 2), (9, 5, 4)), 10)
        decisiones = [p["decision"] for p in r["traza"]["reconstruccion"]]
        self.assertEqual(decisiones, ["acelerar", "no acelerar", "acelerar"])
        self.assertEqual(r["traza"]["reconstruccion"][-1]["presupuesto_restante"], 1)

    def test_almuerzo(self):
        r = resolver(etapas((6, 1, 6), (10, 2, 10), (12, 3, 12)), 5)
        self.assertEqual(r["etapas_aceleradas"], [2, 3])
        self.assertEqual(r["reduccion"], 22)
        self.assertEqual(r["traza"]["tabla"][3], [0, 6, 10, 16, 18, 22])


class CasosBorde(unittest.TestCase):
    def test_presupuesto_cero(self):
        r = resolver(etapas((5, 1, 2)), 0)
        self.assertEqual(r["etapas_aceleradas"], [])
        self.assertEqual(r["duracion_final"], 5)

    def test_sin_etapas(self):
        r = resolver([], 10)
        self.assertEqual(r["etapas_aceleradas"], [])
        self.assertEqual(r["duracion_final"], 0)

    def test_costo_mayor_al_presupuesto(self):
        self.assertEqual(resolver(etapas((5, 9, 2)), 3)["etapas_aceleradas"], [])

    def test_costo_cero(self):
        self.assertEqual(resolver(etapas((5, 0, 2)), 0)["etapas_aceleradas"], [1])


class ContraFuerzaBruta(unittest.TestCase):
    def test_casos_aleatorios(self):
        rng = random.Random(2026)
        for _ in range(300):
            lista = []
            for _ in range(rng.randint(0, 10)):
                t = rng.randint(0, 20)
                lista.append({"t": t, "c": rng.randint(0, 15), "d": rng.randint(0, t)})
            presupuesto = rng.randint(0, 40)

            r = resolver(lista, presupuesto)
            self.assertEqual(r["reduccion"], fuerza_bruta(lista, presupuesto))
            self.assertLessEqual(r["costo_usado"], presupuesto)
            self.assertEqual(
                sum(lista[i - 1]["d"] for i in r["etapas_aceleradas"]), r["reduccion"]
            )


class Validacion(unittest.TestCase):
    def test_d_mayor_que_t(self):
        caso = {"id": "x", "B": 5, "etapas": [{"t": 2, "c": 1, "d": 3}]}
        with self.assertRaises(CasoInvalido):
            validar_caso(caso)

    def test_presupuesto_no_entero(self):
        with self.assertRaises(CasoInvalido):
            validar_caso({"id": "x", "B": 2.5, "etapas": []})


if __name__ == "__main__":
    unittest.main()
