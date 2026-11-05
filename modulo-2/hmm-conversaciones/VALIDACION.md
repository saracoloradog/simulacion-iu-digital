# Validación de la implementación y los resultados

## Algoritmos

- Ocho pruebas Python aprobadas: enumeración exhaustiva para Forward y Viterbi,
  probabilidades y dimensiones, símbolos inválidos, secuencias imposibles,
  caso determinista, reproducibilidad y estabilidad en 10.000 observaciones.
- Tres referencias de 100 turnos coinciden entre Python y JavaScript en estados,
  símbolos y trayectoria Viterbi. Forward coincide a 1e-10 y el filtro a 1e-12.
- Comandos: `python -m unittest discover -s tests -v` y
  `node tests/concordancia.cjs`.

## Experimentos

Se ejecutaron 3.000 réplicas principales y 3.750 de sensibilidad, con 100 turnos
por réplica. La repetición completa produjo los mismos ocho CSV: sus huellas
se conservan en `resultados/reproducibilidad.json`.

Las tablas del artículo se contrastaron con los CSV. La revisión editorial
conserva sus celdas numéricas, las matrices, las cinco figuras y los algoritmos.
Los IC principales se recalcularon a partir de las réplicas con t de Student.
La ocupación esperada se comprueba además mediante la media de πA^t.

## Documentos y laboratorios

El informe HTML y el PDF se generan desde `articulo/contenido.json` y
`articulo/metadatos.json`. El PDF tiene 13 páginas y fue renderizado para
comprobar tablas, imágenes y límites. La fuente LaTeX se genera junto con él;
el PDF distribuido se produce con ReportLab.

Los dos laboratorios conservan su modelo y controles. El simulador permite
observar prefijos y comparar estados. El laboratorio calcula estadísticas,
confusión y sensibilidad, y prepara un CSV con parámetros y semillas.

## Alcance

Los resultados evalúan una simulación con parámetros conocidos. No se utilizan
conversaciones reales ni se mide un desenlace de abandono efectivo. Los IC
representan variabilidad Montecarlo; las limitaciones se explican en el artículo.
