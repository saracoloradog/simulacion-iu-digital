# Estados conversacionales latentes y riesgo de abandono mediante HMM

**Sara Colorado Gil · IU Digital de Antioquia · Ingeniería de Software y Datos**  
Simulación, actividad didáctica 2, módulo 2. Docente: Julián Andrés Loaiza López. 2026.

## Problema y objetivos

Estudiar cómo un HMM discreto representa regímenes conversacionales y cómo la
transición, emisión y distribución inicial afectan inferencia y reproducibilidad.
Se usa una **verdad sintética conocida**, sin datos personales ni entrenamiento.
El objetivo verificable es implementar y comprobar una simulación reproducible.

## Acceso

- [Informe](https://saracoloradog.github.io/simulacion-iu-digital/modulo-2/hmm-conversaciones/)
- [Simulador](https://saracoloradog.github.io/simulacion-iu-digital/modulo-2/hmm-conversaciones/demo.html)
- [Laboratorio](https://saracoloradog.github.io/simulacion-iu-digital/modulo-2/hmm-conversaciones/laboratorio.html)
- [PDF](articulo/articulo.pdf), [LaTeX](articulo/articulo.tex)

## Modelo

S1: avance positivo; S2: fricción; S3: riesgo. Son regímenes operacionales,
no emociones diagnosticadas. Cinco símbolos: confirmación, información,
aclaración, objeción y pausa. La pausa es temporal; no termina la secuencia.
El horizonte fijo produce censura administrativa y **no representa abandono real**.

`modelos.json` centraliza A (3×3 por escenario), B (3×5 compartida) y π.
Convención fila-estocástica: filas suman uno. La comparación A/B/C cambia
solamente A. Los números son supuestos sintéticos justificados en el informe.
Forward escalado devuelve log-verosimilitud y filtro causal; Viterbi en logaritmos
reconstruye el MAP de la trayectoria completa y no es un pronóstico.

## Estructura

```text
index.html / demo.html / laboratorio.html   Informe y dos laboratorios
hmm.js / app.js / style.css                  Algoritmos e interfaz web
modelos.json                                Parámetros compartidos
src/modelo_hmm.py                           Validación, LCG, Forward, Viterbi
src/simulador.py                            Carga del modelo
src/experimentos.py                         Réplicas, IC, sensibilidad y figuras
src/crear_articulo.py                       PDF y fuente LaTeX
articulo/contenido.json                     Contenido estructurado del manuscrito
articulo/referencias.json                   Once publicaciones + fuentes docentes en informe
resultados/                                 Réplicas, resúmenes, confusión, referencias y manifiesto
figuras/                                    PNG a 300 dpi
 tests/                                     Pruebas Python y concordancia JS
VALIDACION.md                              Pruebas y reproducibilidad
```

## Instalación y ejecución

Python 3.10 o superior; Node.js 18+ solo para pruebas de concordancia.
Desde esta carpeta:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/experimentos.py
node tests/concordancia.cjs
python src/crear_articulo.py
python -m http.server 8000
```

Abrir `http://localhost:8000/`. Los laboratorios funcionan con JavaScript
sin backend ni bibliotecas remotas. El servidor local permite cargar JSON;
no se recomienda `file://`. Para regenerar el HTML desde el contenido
estructurado se incluye `python src/crear_html.py`.
El PDF se genera con ReportLab, sin necesitar TeX. Para compilar la alternativa
LaTeX en Overleaf, cargar toda la carpeta y elegir **XeLaTeX**, archivo principal
`articulo/articulo.tex`. La fuente LaTeX no fue compilada en el entorno de creación.

## Experimentos y resultados

Semilla maestra: **20261105**. 1.000 réplicas por escenario, T=100.
Las mismas semillas se reutilizan entre escenarios para permitir comparaciones
emparejadas. Cada réplica conserva su semilla en el CSV.

| Escenario | Ocupación de riesgo | Exactitud Viterbi |
|---|---:|---:|
| A · estable | 6,941 % | 80,176 % |
| B · fricción | 50,933 % | 67,664 % |
| C · recuperación | 5,412 % | 77,758 % |

`resumen.csv` contiene media, DE muestral, mínimo, máximo, n válido e IC95 % t
sobre **réplicas**, sin tratar turnos correlacionados como independientes.
Hay 3.750 réplicas adicionales de sensibilidad: tres factores, cinco niveles,
250 corridas por nivel. Se registra también exactitud con decodificador nominal.
Las figuras de ocupación, confusión, trayectoria y sensibilidad provienen de
las corridas que generaron los CSV. El manifiesto incluye versiones y SHA-256.

## Reproducibilidad entre lenguajes

LCG32 compartido: `x = (1664525*x + 1013904223) mod 2^32` y `u=x/2^32`.
Cada turno consume estado y luego observación. Las tres referencias de cien
turnos coinciden exactamente en estados, símbolos y ruta Viterbi; Forward y
filtrado coinciden con tolerancias 1e-10 y 1e-12. Los empates favorecen el índice
menor. No se promete independencia formal entre subflujos de este LCG.

Python obtiene las semillas de réplica con NumPy SeedSequence. El laboratorio
web las obtiene del LCG, por lo que sus corridas agregadas son distintas.
Los IC web usan 1,96 (mínimo 30 corridas); Python usa t de Student.

## Limitaciones y pendientes humanos

No hay corpus real, eventos terminales, entrenamiento ni validación externa.
La exactitud con parámetros conocidos es favorable y depende del desbalance.
Las duraciones incluyen episodios censurados en bordes; corridas sin riesgo
se excluyen solo de la media de duración. Los IC cubren variabilidad Montecarlo,
no incertidumbre del modelo. La revisión de once publicaciones es dirigida,
no sistemática, y no certifica indexación individual en Scopus/WoS.

Debe grabarse el video de máximo tres minutos, incorporar su enlace y subir
el PDF a Canvas antes del **8 de noviembre de 2026, 11:59 p. m. (Colombia)**.
No se afirma que estos pasos humanos estén realizados. Consultar `VALIDACION.md` para
el estado comprobado de publicación y controles.
