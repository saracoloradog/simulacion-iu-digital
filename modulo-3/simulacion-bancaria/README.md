# Simulación de atención bancaria

**Sara Colorado Gil · IU Digital de Antioquia · Ingeniería de Software y Datos**
Asignatura: Simulación. Actividad didáctica 2, módulo 3. 2026.

## Propósito

El banco tiene tres cajas y necesita decidir si conviene dedicar dos a retiros
y una a pagos, o una a retiros y dos a pagos. La actividad también pide revisar
si una cuarta caja reduciría suficientemente los tiempos de espera.

Este proyecto simula cien días de ocho horas. En cada réplica se generan los
mismos clientes para las cuatro configuraciones, de modo que la comparación no
dependa de que un escenario haya recibido una demanda más fácil por casualidad.

## Escenarios

- Tres cajas mixtas, como referencia.
- Dos cajas de retiro y una de pago.
- Una caja de retiro y dos de pago.
- Dos cajas de retiro y dos de pago, para evaluar una caja adicional.

## Supuestos adoptados

1. El 70 % de los clientes realiza retiros y el 30 % realiza pagos.
2. Primero se selecciona la acción y el tipo del próximo cliente. Después se
   genera el tiempo entre llegadas con la media de la tabla del enunciado.
3. Los tiempos de servicio son exponenciales y dependen de la acción y del tipo
   de usuario.
4. Cada cajero mantiene una fila FIFO. El cliente elige el cajero compatible
   que pueda comenzar a atenderlo primero.
5. A las 480 minutos dejan de llegar personas. El banco termina de atender a
   quienes llegaron antes del cierre; ese tiempo adicional se registra.
6. Todos los cajeros tienen la misma capacidad. Las diferencias observadas se
   deben a los clientes asignados y no a una habilidad distinta del empleado.

La mezcla de medias por tipo hace que el sistema agregado no sea un M/M/1 puro.
Se conserva el supuesto exponencial condicionado al tipo y se usa simulación de
eventos discretos. Esta limitación se explicará en el informe.

## Resultados principales

| Configuración | Espera media | Utilización máxima media |
|---|---:|---:|
| 3 cajas mixtas | 0,44 min | 47,6 % |
| 2 retiros + 1 pago | 3,03 min | 63,7 % |
| 1 retiro + 2 pagos | 4,36 min | 67,1 % |
| 2 retiros + 2 pagos | 0,44 min | 38,8 % |

Entre las dos alternativas de cajas exclusivas, `2 retiros + 1 pago` obtuvo la
menor espera global. Sin embargo, los pagos esperaron 9,41 minutos en promedio.
La cuarta caja equilibra las operaciones, pero no es necesaria para mantener el
sistema estable. Si se permiten cajas mixtas, tres cajeros alcanzan prácticamente
la misma espera que cuatro cajas especializadas.

El [informe web](index.html) presenta las tablas y gráficas con una explicación
del alcance de esta recomendación.

## Estructura

```text
src/simulacion_bancaria.py     Generación de demanda y atención de clientes
src/experimentos.py            Réplicas, resúmenes CSV y gráficas
tests/test_simulacion.py       Pruebas de reproducibilidad y lógica de filas
resultados/                    Datos producidos por las cien réplicas
figuras/                       Imágenes utilizadas en el informe
```

## Ejecución

Desde esta carpeta:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/experimentos.py
```

Para ejecutar únicamente las diez réplicas mínimas solicitadas:

```bash
python src/experimentos.py 10
```

La semilla maestra es `20261122`. Los CSV guardan la semilla de cada réplica.
El simulador no publica datos personales y utiliza únicamente clientes
sintéticos.
