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

## Módulo 2: conversaciones y Modelos Ocultos de Markov

Simulación de tres escenarios conversacionales con Forward, Viterbi y análisis
de sensibilidad. Los resultados proceden de experimentos con datos sintéticos.

- [Informe académico](https://saracoloradog.github.io/simulacion-iu-digital/modulo-2/hmm-conversaciones/)
- [Simulador conversacional](https://saracoloradog.github.io/simulacion-iu-digital/modulo-2/hmm-conversaciones/demo.html)
- [Laboratorio HMM](https://saracoloradog.github.io/simulacion-iu-digital/modulo-2/hmm-conversaciones/laboratorio.html)
- [Artículo PDF](modulo-2/hmm-conversaciones/articulo/articulo.pdf)
- [Código, resultados e instrucciones](modulo-2/hmm-conversaciones/README.md)

## Módulo 3: simulación de atención bancaria

Simulación de eventos discretos para comparar la distribución de tres cajas
entre operaciones de retiros y pagos. Se simularon 100 jornadas de ocho horas
con tiempos de llegada y servicio exponenciales según el tipo de usuario.

Se analizaron cuatro configuraciones: tres cajas mixtas, dos para retiros y una
para pagos, una para retiros y dos para pagos, y una alternativa de cuatro cajas.
Entre las dos opciones con cajas exclusivas, la menor espera general se obtuvo
con dos cajas para retiros y una para pagos.

- [Informe académico](https://saracoloradog.github.io/simulacion-iu-digital/modulo-3/simulacion-bancaria/)
- [Código de la simulación](modulo-3/simulacion-bancaria/src/simulacion_bancaria.py)
- [Resultados de los escenarios](modulo-3/simulacion-bancaria/resultados/resumen_escenarios.csv)
- [Código, metodología e instrucciones](modulo-3/simulacion-bancaria/README.md)
