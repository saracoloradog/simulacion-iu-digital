import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from simulacion_bancaria import (  # noqa: E402
    Cliente,
    ESCENARIOS,
    generar_demanda,
    medias_teoricas,
    simular_escenario,
)


class TestSimulacionBancaria(unittest.TestCase):
    def test_demanda_reproducible(self):
        a = generar_demanda(np.random.default_rng(42))
        b = generar_demanda(np.random.default_rng(42))
        self.assertEqual(a, b)

    def test_llegadas_ocurren_durante_apertura(self):
        clientes = generar_demanda(np.random.default_rng(7))
        self.assertTrue(clientes)
        self.assertTrue(all(0 <= c.llegada <= 480 for c in clientes))
        self.assertTrue(all(a.llegada < b.llegada for a, b in zip(clientes, clientes[1:])))

    def test_escenarios_atienden_la_misma_demanda(self):
        clientes = generar_demanda(np.random.default_rng(19))
        for escenario in ESCENARIOS:
            registros, _ = simular_escenario(clientes, escenario)
            self.assertEqual(len(registros), len(clientes))
            self.assertTrue(all(r["tiempo_espera"] >= 0 for r in registros))

    def test_cajero_respeta_especialidad(self):
        clientes = generar_demanda(np.random.default_rng(31))
        for escenario in ("2_retiro_1_pago", "1_retiro_2_pago", "2_retiro_2_pago"):
            registros, _ = simular_escenario(clientes, escenario)
            for registro in registros:
                self.assertEqual(registro["accion"], registro["especialidad"])

    def test_fifo_en_un_cajero(self):
        clientes = [
            Cliente(1, 1.0, "retiro", "rapido", 5.0, 0.0),
            Cliente(2, 2.0, "retiro", "rapido", 1.0, 0.0),
        ]
        registros, _ = simular_escenario(clientes, "1_retiro_2_pago")
        self.assertEqual(registros[0]["inicio_servicio"], 1.0)
        self.assertEqual(registros[1]["inicio_servicio"], 6.0)
        self.assertEqual(registros[1]["tiempo_espera"], 4.0)

    def test_medias_ponderadas(self):
        medias = medias_teoricas()
        self.assertAlmostEqual(medias["media_servicio_retiro"], 2.34)
        self.assertAlmostEqual(medias["media_servicio_pago"], 5.20)
        self.assertAlmostEqual(medias["media_llegada_total"], 2.398)


if __name__ == "__main__":
    unittest.main()
