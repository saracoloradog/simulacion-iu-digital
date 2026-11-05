# Registro de aseguramiento de calidad

Fecha: 5 de noviembre de 2026 (Colombia). Datos exclusivamente sintéticos.

## Comprobaciones ejecutadas

- **Python:** 8 pruebas aprobadas. Forward y Viterbi contrastados con enumeración
  exhaustiva de las 16 secuencias binarias de longitud 4 y sus 16 trayectorias;
  validación de probabilidades, símbolos inválidos, ceros/imposibilidad,
  reproducibilidad, caso determinista y Forward de 10.000 observaciones.
  Registro: `resultados/pruebas_python.txt`.
- **Concordancia JS/Python:** 3 casos de 100 turnos; estados, observaciones y
  trayectorias idénticos. log-verosimilitud y puntuación Viterbi a 1e-10;
  filtro a 1e-12. Validación y casos imposibles aprobados.
  Registro: `resultados/pruebas_concordancia.txt`.
- **Experimentos ejecutados:** 3.000 réplicas principales y 3.750 de sensibilidad;
  675.000 turnos. Las figuras PNG a 300 dpi proceden de esas mismas corridas.
- **Reejecución completa:** los ocho CSV resultaron idénticos byte por byte
  (SHA-256). Registro: `resultados/reproducibilidad.json`.
- **Contraste analítico:** ocupación esperada calculada con la media de πA^t,
  t=0…99; `resultados/esperanza_exacta.csv`. No se exige que todos los
  valores teóricos queden dentro de cada IC95 % de una realización.
- **Interfaz de laboratorio:** 300 réplicas × 50 turnos ejecutadas en navegador;
  estadísticas y confusión calculadas. Sensibilidad de cinco niveles ejecutada.
  Se comprobó rechazo de fila de suma 1,10 y restablecimiento del escenario.
- **CSV web:** botón accionado, Blob preparado y enlace de descarga con nombre
  `hmm_replicas.csv` verificado. Incluye matrices y semillas para reproducibilidad.
  El evento de descarga del navegador integrado no pudo verificarse por esa API;
  se dejó un enlace visible como alternativa a la descarga automática.
- **Simulador:** avance de prefijo, revelación/ocultación, mostrar todos y botón
  siguiente desactivado al alcanzar T. Las etiquetas Viterbi se recalculan por prefijo.
- **Responsive:** informe revisado a 1280×900 y 390×844; sin desbordamiento
  horizontal a 390 px después de ajustar enlaces largos. Laboratorio a 390 px
  sin desbordamiento del documento. Tablas y secuencias tienen desplazamiento propio.
- **Figuras web:** cinco imágenes cargadas correctamente.
- **PDF:** 17 páginas renderizadas e inspeccionadas mediante contacto de todas
  las páginas y ampliaciones de portada, modelo y resultados. Texto dentro de
  los límites de página; tablas y figuras sin recortes. 13 páginas de contenido,
  portada, dos de referencias y anexo. Generación con ReportLab.
- **HTML de impresión:** alturas automáticas, títulos unidos al contenido,
  tablas/figuras con control de salto y márgenes A4. No se generó una segunda
  copia PDF mediante el diálogo de impresión del navegador.
- **Fuentes:** once publicaciones 2022–2025 verificadas en páginas originales.
  Se distingue HMM de antecedentes de contexto; no se certifica indexación
  individual Scopus/WoS. Los ejemplos docentes no se tratan como resultados propios.
- **Módulo 1:** se comprueba ausencia de cambios en sus HTML y carpeta; solo se
  agrega una sección al README principal.

## Publicación

Conexión verificada: GitHub **IU Digital**, usuario **saracoloradog**.
Repositorio público y permiso de escritura comprobados mediante el conector.
El estado del despliegue y sus rutas se registrará después de publicar.

## Pendientes humanos y límites

- Grabar el video (máximo tres minutos), cargarlo e incorporar el enlace.
- Subir el artículo PDF a Canvas antes del 8 de noviembre de 2026, 23:59 Colombia.
- La fuente LaTeX se entrega para XeLaTeX/Overleaf; no se compiló con TeX aquí.
- El proyecto no estima abandono observado, no usa conversaciones reales y no
  valida rendimiento en producción. Los IC representan error Montecarlo.
