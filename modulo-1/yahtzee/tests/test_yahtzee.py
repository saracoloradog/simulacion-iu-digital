import unittest
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from yahtzee_montecarlo import lanzar_dados, puntuar, total, montecarlo


class PruebasYahtzee(unittest.TestCase):
    def test_valores_del_dado(self):
        dados = lanzar_dados(random.Random(10))
        self.assertEqual(len(dados), 5)
        self.assertTrue(all(1 <= valor <= 6 for valor in dados))

    def test_conservar_dados(self):
        original = [6, 6, 2, 3, 4]
        resultado = lanzar_dados(random.Random(7), original, [True, True, False, False, False])
        self.assertEqual(resultado[:2], [6, 6])

    def test_yahtzee(self):
        self.assertEqual(puntuar([3, 3, 3, 3, 3], "yahtzee"), 50)
        self.assertEqual(puntuar([3, 3, 3, 3, 4], "yahtzee"), 0)

    def test_full(self):
        self.assertEqual(puntuar([2, 2, 2, 5, 5], "full"), 25)

    def test_escaleras(self):
        self.assertEqual(puntuar([1, 2, 3, 4, 6], "escalera_menor"), 30)
        self.assertEqual(puntuar([1, 2, 3, 4, 5], "escalera_mayor"), 40)

    def test_bono(self):
        self.assertEqual(total(dict(zip(["unos", "doses", "treses", "cuatros", "cincos", "seises"], [3, 6, 9, 12, 15, 18]))), 98)

    def test_montecarlo_repetible(self):
        self.assertEqual(montecarlo(100, 2026), montecarlo(100, 2026))


if __name__ == "__main__":
    unittest.main()
