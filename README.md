# Simulación · IU Digital 🎲

Repositorio de la materia **Simulación** de la IU Digital de Antioquia.

## Módulo 1: Yahtzee y Montecarlo

En esta actividad desarrollé un juego de Yahtzee para dos jugadores y un experimento de Montecarlo para comparar las frecuencias de los dados con sus probabilidades teóricas.

## 🎥 Video de sustentación

**[▶️ VER VIDEO DE SUSTENTACIÓN EN GOOGLE DRIVE](https://drive.google.com/file/d/1gqFkcGyxMB93lJUQeaNJ2_ODZk-kNphH/view?usp=sharing)**

En el video se presenta el funcionamiento del juego de Yahtzee y se explican la simulación de Montecarlo, el algoritmo y los resultados obtenidos.

## 🌐 Ver la entrega interactiva

**[👉 ABRIR EL INFORME ACADÉMICO (sitio web, no código)](https://saracoloradog.github.io/simulacion-iu-digital/)**

Desde el informe se puede acceder al juego y al laboratorio de Montecarlo.

- [Informe académico web — ver presentación](https://saracoloradog.github.io/simulacion-iu-digital/)
- [Jugar Yahtzee — abrir juego](https://saracoloradog.github.io/simulacion-iu-digital/demo.html)
- [Laboratorio Montecarlo — abrir simulador](https://saracoloradog.github.io/simulacion-iu-digital/laboratorio.html)
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

La página del laboratorio permite ejecutar entre 100 y 100.000 lanzamientos, observar las frecuencias y exportar un CSV. Está construida en JavaScript y funciona sin servidor.
