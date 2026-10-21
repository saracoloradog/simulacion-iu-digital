# Simulación · IU Digital 🎲

Repositorio de la materia **Simulación** de la IU Digital de Antioquia.

## Módulo 1: Yahtzee y Montecarlo

En esta actividad desarrollé un juego de Yahtzee para dos jugadores y un experimento de Montecarlo para comparar las frecuencias de los dados con sus probabilidades teóricas.

- [Informe académico web](index.html)
- [Juego visual de Yahtzee](demo.html)
- [Implementación en Python](modulo-1/yahtzee/yahtzee_montecarlo.py)
- [Pruebas](modulo-1/yahtzee/tests/test_yahtzee.py)

### Ejecución

Requiere Python 3, sin librerías adicionales.

```bash
python modulo-1/yahtzee/yahtzee_montecarlo.py --jugar
python modulo-1/yahtzee/yahtzee_montecarlo.py --simulaciones 100000 --semilla 2026
python -m unittest discover -s modulo-1/yahtzee/tests
```

El experimento de Montecarlo repite **lanzamientos independientes de cinco dados**. No equivale a calcular la probabilidad de ganar después de los tres intentos de una partida, donde también influye la estrategia.

**Autora:** Sara Colorado Gil.
