import argparse
import csv
import random
from collections import Counter

CATEGORIAS = ["unos", "doses", "treses", "cuatros", "cincos", "seises", "tercia", "poker", "full", "escalera_menor", "escalera_mayor", "yahtzee", "chance"]

def lanzar_dados(rng, dados=None, conservar=None):
    dados = dados if dados is not None else [0] * 5
    conservar = conservar if conservar is not None else [False] * 5
    if len(dados) != 5 or len(conservar) != 5:
        raise ValueError("Se necesitan cinco dados")
    return [dados[i] if conservar[i] else rng.randint(1, 6) for i in range(5)]

def puntuar(dados, categoria):
    if len(dados) != 5 or any(d not in range(1, 7) for d in dados):
        raise ValueError("Los dados deben estar entre 1 y 6")
    if categoria not in CATEGORIAS:
        raise ValueError("Categoría desconocida")
    cuentas = Counter(dados)
    if categoria in CATEGORIAS[:6]:
        numero = CATEGORIAS.index(categoria) + 1
        return numero * cuentas[numero]
    if categoria == "tercia":
        return sum(dados) if max(cuentas.values()) >= 3 else 0
    if categoria == "poker":
        return sum(dados) if max(cuentas.values()) >= 4 else 0
    if categoria == "full":
        return 25 if sorted(cuentas.values()) == [2, 3] else 0
    if categoria == "escalera_menor":
        return 30 if any(set(range(i, i + 4)) <= set(dados) for i in (1, 2, 3)) else 0
    if categoria == "escalera_mayor":
        return 40 if set(dados) in ({1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}) else 0
    if categoria == "yahtzee":
        return 50 if len(cuentas) == 1 else 0
    return sum(dados)

def total(tarjeta):
    superior = sum(tarjeta.get(c, 0) for c in CATEGORIAS[:6])
    return sum(tarjeta.values()) + (35 if superior >= 63 else 0)

def jugar(rng):
    jugadores = [{"nombre": "Jugador 1", "tarjeta": {}}, {"nombre": "Jugador 2", "tarjeta": {}}]
    for ronda in range(1, 14):
        for jugador in jugadores:
            dados = lanzar_dados(rng)
            print("\n", jugador["nombre"], "| Ronda", ronda)
            for tiro in range(1, 4):
                print("Lanzamiento", tiro, dados)
                if tiro == 3:
                    break
                respuesta = input("Conservar posiciones (ej. 1,3), Enter para relanzar todo o FIN para anotar: ").strip()
                if respuesta.lower() == "fin":
                    break
                try:
                    posiciones = {int(i.strip()) for i in respuesta.split(",") if i.strip()}
                    if not posiciones <= {1, 2, 3, 4, 5}:
                        raise ValueError
                except ValueError:
                    print("Selección inválida; se relanzarán todos")
                    posiciones = set()
                dados = lanzar_dados(rng, dados, [i + 1 in posiciones for i in range(5)])
            opciones = [c for c in CATEGORIAS if c not in jugador["tarjeta"]]
            for num, c in enumerate(opciones, 1):
                print(num, c, ":", puntuar(dados, c))
            while True:
                try:
                    eleccion = int(input("Selecciona categoría: "))
                    if 1 <= eleccion <= len(opciones):
                        break
                except ValueError:
                    pass
                print("Elige una opción válida")
            categoria = opciones[eleccion - 1]
            jugador["tarjeta"][categoria] = puntuar(dados, categoria)
            print("Puntaje acumulado:", total(jugador["tarjeta"]))
    a, b = (total(j["tarjeta"]) for j in jugadores)
    print("\nResultado:", a, "-", b)
    print("Empate" if a == b else "Ganó Jugador 1" if a > b else "Ganó Jugador 2")

def montecarlo(n, semilla, archivo=None):
    if n <= 0:
        raise ValueError("Las simulaciones deben ser positivas")
    rng = random.Random(semilla)
    frecuencias = Counter()
    yahtzees = 0
    for _ in range(n):
        dados = lanzar_dados(rng)
        frecuencias.update(dados)
        yahtzees += len(set(dados)) == 1
    print("Simulaciones:", n, "| Semilla:", semilla)
    print("Cara | Observados | Frecuencia relativa | Valor teórico")
    filas = []
    for cara in range(1, 7):
        prop = frecuencias[cara] / (5 * n)
        print(cara, frecuencias[cara], f"{prop:.4%}", f"{1/6:.4%}")
        filas.append(["cara", cara, frecuencias[cara], prop, 1/6])
    print("Yahtzee en un lanzamiento:", yahtzees, f"({yahtzees/n:.5%}); teoría: {1/1296:.5%}")
    filas.append(["yahtzee", "cinco iguales", yahtzees, yahtzees / n, 1 / 1296])
    if archivo:
        with open(archivo, "w", newline="", encoding="utf-8") as salida:
            csv.writer(salida).writerows([["tipo", "valor", "casos", "proporcion", "teorica"], *filas])
    return frecuencias, yahtzees

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jugar", action="store_true")
    parser.add_argument("--simulaciones", type=int, default=100000)
    parser.add_argument("--semilla", type=int, default=2026)
    parser.add_argument("--exportar")
    args = parser.parse_args()
    if args.jugar:
        jugar(random.Random(args.semilla))
    else:
        montecarlo(args.simulaciones, args.semilla, args.exportar)
