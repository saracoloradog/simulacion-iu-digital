"""Simulación de la atención de una sucursal bancaria.

El módulo separa la generación de la demanda de la asignación de cajeros. De
esta forma, una misma réplica se puede probar con varias configuraciones sin
que cambien los clientes, sus llegadas ni sus tiempos de servicio.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


TIPOS_USUARIO = ("rapido", "normal", "lento", "muy_lento")

PROBABILIDAD_ACCION = {"retiro": 0.70, "pago": 0.30}
PROBABILIDAD_USUARIO = {
    "retiro": np.array([0.23, 0.40, 0.17, 0.20]),
    "pago": np.array([0.10, 0.20, 0.30, 0.40]),
}
MEDIA_LLEGADA = {
    "retiro": np.array([1.0, 2.0, 3.0, 3.0]),
    "pago": np.array([1.0, 2.0, 3.0, 4.0]),
}
MEDIA_SERVICIO = {
    "retiro": np.array([1.0, 2.0, 3.0, 4.0]),
    "pago": np.array([3.0, 3.0, 5.0, 7.0]),
}

# Cada tupla contiene (identificador, servicio permitido). "mixto" atiende
# cualquiera de las dos operaciones.
ESCENARIOS = {
    "3_mixtos": (("M1", "mixto"), ("M2", "mixto"), ("M3", "mixto")),
    "2_retiro_1_pago": (("R1", "retiro"), ("R2", "retiro"), ("P1", "pago")),
    "1_retiro_2_pago": (("R1", "retiro"), ("P1", "pago"), ("P2", "pago")),
    "2_retiro_2_pago": (
        ("R1", "retiro"),
        ("R2", "retiro"),
        ("P1", "pago"),
        ("P2", "pago"),
    ),
}


@dataclass(frozen=True)
class Cliente:
    identificador: int
    llegada: float
    accion: str
    tipo: str
    servicio: float
    desempate: float


def generar_demanda(
    rng: np.random.Generator, minutos_operacion: float = 480.0
) -> list[Cliente]:
    """Genera una corriente de clientes hasta el cierre de la sucursal.

    Se sigue la interpretación usada por el ejemplo docente: primero se elige
    la acción y el tipo del próximo cliente; después se genera su tiempo entre
    llegadas con la media indicada en la tabla. El resultado es una mezcla de
    exponenciales, lo cual se documenta como una aproximación al M/M/1.
    """

    clientes: list[Cliente] = []
    tiempo = 0.0

    while True:
        accion = "retiro" if rng.random() < PROBABILIDAD_ACCION["retiro"] else "pago"
        indice = int(rng.choice(len(TIPOS_USUARIO), p=PROBABILIDAD_USUARIO[accion]))
        tiempo += float(rng.exponential(MEDIA_LLEGADA[accion][indice]))
        if tiempo > minutos_operacion:
            break

        clientes.append(
            Cliente(
                identificador=len(clientes) + 1,
                llegada=tiempo,
                accion=accion,
                tipo=TIPOS_USUARIO[indice],
                servicio=float(rng.exponential(MEDIA_SERVICIO[accion][indice])),
                desempate=float(rng.random()),
            )
        )

    return clientes


def _cajeros_elegibles(accion: str, configuracion: tuple[tuple[str, str], ...]) -> list[int]:
    return [
        indice
        for indice, (_, servicio) in enumerate(configuracion)
        if servicio == "mixto" or servicio == accion
    ]


def simular_escenario(
    clientes: Iterable[Cliente],
    escenario: str,
    minutos_operacion: float = 480.0,
) -> tuple[list[dict], list[dict]]:
    """Atiende los clientes en filas FIFO independientes por cajero.

    El cliente se dirige al cajero compatible que pueda comenzar a atenderlo
    primero. En un empate se usa un número previamente generado para conservar
    la comparación justa entre escenarios.
    """

    if escenario not in ESCENARIOS:
        raise ValueError(f"Escenario desconocido: {escenario}")

    configuracion = ESCENARIOS[escenario]
    disponibles = np.zeros(len(configuracion), dtype=float)
    ocupacion_apertura = np.zeros(len(configuracion), dtype=float)
    registros: list[dict] = []

    for cliente in clientes:
        elegibles = _cajeros_elegibles(cliente.accion, configuracion)
        if not elegibles:
            raise ValueError(f"No hay cajero para la acción {cliente.accion}")

        inicio_posible = np.array(
            [max(cliente.llegada, disponibles[i]) for i in elegibles]
        )
        minimo = float(inicio_posible.min())
        empatados = [
            elegibles[i]
            for i, valor in enumerate(inicio_posible)
            if np.isclose(valor, minimo)
        ]
        elegido = empatados[min(int(cliente.desempate * len(empatados)), len(empatados) - 1)]

        inicio = max(cliente.llegada, disponibles[elegido])
        fin = inicio + cliente.servicio
        disponibles[elegido] = fin

        # Solo se cuenta como utilización la parte del servicio que ocurre
        # dentro de las ocho horas. La fila pendiente se termina de atender.
        if inicio < minutos_operacion:
            ocupacion_apertura[elegido] += max(
                0.0, min(fin, minutos_operacion) - inicio
            )

        identificador_cajero, especialidad = configuracion[elegido]
        registros.append(
            {
                "cliente": cliente.identificador,
                "accion": cliente.accion,
                "tipo_usuario": cliente.tipo,
                "llegada": cliente.llegada,
                "tiempo_servicio": cliente.servicio,
                "cajero": identificador_cajero,
                "especialidad": especialidad,
                "inicio_servicio": inicio,
                "fin_servicio": fin,
                "tiempo_espera": inicio - cliente.llegada,
                "tiempo_sistema": fin - cliente.llegada,
            }
        )

    ultimo_fin = float(disponibles.max()) if len(disponibles) else 0.0
    resumen_cajeros = []
    for indice, (identificador, especialidad) in enumerate(configuracion):
        atendidos = [r for r in registros if r["cajero"] == identificador]
        resumen_cajeros.append(
            {
                "cajero": identificador,
                "especialidad": especialidad,
                "usuarios": len(atendidos),
                "tiempo_servicio_promedio": (
                    float(np.mean([r["tiempo_servicio"] for r in atendidos]))
                    if atendidos
                    else np.nan
                ),
                "tiempo_espera_promedio": (
                    float(np.mean([r["tiempo_espera"] for r in atendidos]))
                    if atendidos
                    else np.nan
                ),
                "utilizacion": ocupacion_apertura[indice] / minutos_operacion,
                "ultimo_fin": disponibles[indice],
                "minutos_extra": max(0.0, disponibles[indice] - minutos_operacion),
                "fin_escenario": ultimo_fin,
            }
        )

    return registros, resumen_cajeros


def medias_teoricas() -> dict[str, float]:
    """Devuelve referencias ponderadas útiles para validar la simulación."""

    llegada_retiro = float(PROBABILIDAD_USUARIO["retiro"] @ MEDIA_LLEGADA["retiro"])
    llegada_pago = float(PROBABILIDAD_USUARIO["pago"] @ MEDIA_LLEGADA["pago"])
    llegada_total = 0.70 * llegada_retiro + 0.30 * llegada_pago
    return {
        "media_llegada_retiro": llegada_retiro,
        "media_llegada_pago": llegada_pago,
        "media_llegada_total": llegada_total,
        "tasa_llegada_hora": 60.0 / llegada_total,
        "media_servicio_retiro": float(
            PROBABILIDAD_USUARIO["retiro"] @ MEDIA_SERVICIO["retiro"]
        ),
        "media_servicio_pago": float(
            PROBABILIDAD_USUARIO["pago"] @ MEDIA_SERVICIO["pago"]
        ),
    }
