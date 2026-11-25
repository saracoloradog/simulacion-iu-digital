"""Ejecuta las réplicas, guarda tablas y genera las figuras del informe."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from simulacion_bancaria import (
    ESCENARIOS,
    TIPOS_USUARIO,
    generar_demanda,
    medias_teoricas,
    simular_escenario,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTADOS = ROOT / "resultados"
FIGURAS = ROOT / "figuras"
COLORES = {
    "3_mixtos": "#203a5e",
    "2_retiro_1_pago": "#08628b",
    "1_retiro_2_pago": "#c82332",
    "2_retiro_2_pago": "#f5bf19",
}
ETIQUETAS = {
    "3_mixtos": "3 cajas mixtas",
    "2_retiro_1_pago": "2 retiros + 1 pago",
    "1_retiro_2_pago": "1 retiro + 2 pagos",
    "2_retiro_2_pago": "2 retiros + 2 pagos",
}


def intervalo_95(valores: pd.Series) -> tuple[float, float, float, float]:
    valores = valores.dropna().astype(float)
    media = float(valores.mean())
    desviacion = float(valores.std(ddof=1))
    margen = 1.96 * desviacion / np.sqrt(len(valores))
    return media, desviacion, media - margen, media + margen


def ejecutar(replicas: int = 100, semilla_maestra: int = 20261122) -> None:
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    FIGURAS.mkdir(parents=True, exist_ok=True)

    semillas = np.random.SeedSequence(semilla_maestra).generate_state(replicas)
    filas_clientes: list[dict] = []
    filas_cajeros: list[dict] = []
    filas_replicas: list[dict] = []
    filas_usuarios: list[dict] = []

    for replica, semilla in enumerate(semillas, start=1):
        demanda = generar_demanda(np.random.default_rng(int(semilla)))

        conteos = Counter((cliente.accion, cliente.tipo) for cliente in demanda)
        for accion in ("retiro", "pago"):
            for tipo in TIPOS_USUARIO:
                filas_usuarios.append(
                    {
                        "replica": replica,
                        "semilla": int(semilla),
                        "accion": accion,
                        "tipo_usuario": tipo,
                        "usuarios": conteos[(accion, tipo)],
                    }
                )

        for escenario in ESCENARIOS:
            clientes, cajeros = simular_escenario(demanda, escenario)
            for fila in clientes:
                filas_clientes.append(
                    {"escenario": escenario, "replica": replica, **fila}
                )
            for fila in cajeros:
                filas_cajeros.append(
                    {"escenario": escenario, "replica": replica, **fila}
                )

            espera = np.array([fila["tiempo_espera"] for fila in clientes])
            sistema = np.array([fila["tiempo_sistema"] for fila in clientes])
            filas_replicas.append(
                {
                    "escenario": escenario,
                    "replica": replica,
                    "semilla": int(semilla),
                    "usuarios": len(clientes),
                    "espera_media": float(espera.mean()),
                    "espera_p95": float(np.quantile(espera, 0.95)),
                    "espera_maxima": float(espera.max()),
                    "sistema_medio": float(sistema.mean()),
                    "utilizacion_media": float(
                        np.mean([fila["utilizacion"] for fila in cajeros])
                    ),
                    "utilizacion_maxima": float(
                        np.max([fila["utilizacion"] for fila in cajeros])
                    ),
                    "minutos_extra": float(
                        max(fila["minutos_extra"] for fila in cajeros)
                    ),
                }
            )

    clientes = pd.DataFrame(filas_clientes)
    cajeros = pd.DataFrame(filas_cajeros)
    por_replica = pd.DataFrame(filas_replicas)
    usuarios = pd.DataFrame(filas_usuarios)

    clientes.to_csv(RESULTADOS / "clientes.csv", index=False)
    cajeros.to_csv(RESULTADOS / "cajeros_por_replica.csv", index=False)
    por_replica.to_csv(RESULTADOS / "replicas.csv", index=False)
    usuarios.to_csv(RESULTADOS / "usuarios_por_replica.csv", index=False)

    resumen = []
    for escenario, grupo in por_replica.groupby("escenario", sort=False):
        for metrica in (
            "usuarios",
            "espera_media",
            "espera_p95",
            "sistema_medio",
            "utilizacion_media",
            "utilizacion_maxima",
            "minutos_extra",
        ):
            media, desviacion, inferior, superior = intervalo_95(grupo[metrica])
            resumen.append(
                {
                    "escenario": escenario,
                    "metrica": metrica,
                    "replicas": len(grupo),
                    "media": media,
                    "desviacion": desviacion,
                    "ic95_inferior": inferior,
                    "ic95_superior": superior,
                }
            )
    resumen_df = pd.DataFrame(resumen)
    resumen_df.to_csv(RESULTADOS / "resumen_escenarios.csv", index=False)

    resumen_cajeros = (
        cajeros.groupby(["escenario", "cajero", "especialidad"], sort=False)
        .agg(
            usuarios_promedio=("usuarios", "mean"),
            servicio_promedio=("tiempo_servicio_promedio", "mean"),
            espera_promedio=("tiempo_espera_promedio", "mean"),
            utilizacion_promedio=("utilizacion", "mean"),
        )
        .reset_index()
    )
    resumen_cajeros.to_csv(RESULTADOS / "resumen_cajeros.csv", index=False)

    resumen_tipo = (
        clientes.groupby(["escenario", "accion", "tipo_usuario"], sort=False)
        .agg(
            usuarios=("cliente", "count"),
            servicio_promedio=("tiempo_servicio", "mean"),
            espera_promedio=("tiempo_espera", "mean"),
            sistema_promedio=("tiempo_sistema", "mean"),
        )
        .reset_index()
    )
    resumen_tipo["usuarios_por_replica"] = resumen_tipo["usuarios"] / replicas
    resumen_tipo.to_csv(RESULTADOS / "resumen_tipos.csv", index=False)

    minimo_por_tipo = usuarios.loc[
        usuarios.groupby(["accion", "tipo_usuario"])["usuarios"].idxmin()
    ].sort_values(["accion", "tipo_usuario"])
    minimo_por_tipo.to_csv(RESULTADOS / "minimos_usuarios.csv", index=False)

    (RESULTADOS / "referencia_teorica.json").write_text(
        json.dumps(
            {
                "semilla_maestra": semilla_maestra,
                "replicas": replicas,
                "minutos_por_dia": 480,
                **medias_teoricas(),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    crear_figuras(por_replica, clientes, cajeros)
    print(
        resumen_df[resumen_df["metrica"].isin(["espera_media", "utilizacion_maxima", "minutos_extra"])].to_string(index=False)
    )


def crear_figuras(
    replicas: pd.DataFrame, clientes: pd.DataFrame, cajeros: pd.DataFrame
) -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 130,
            "savefig.dpi": 240,
        }
    )

    orden = list(ESCENARIOS)
    medias = replicas.groupby("escenario")["espera_media"].mean().reindex(orden)
    errores = (
        1.96
        * replicas.groupby("escenario")["espera_media"].std().reindex(orden)
        / np.sqrt(replicas.groupby("escenario").size().reindex(orden))
    )
    fig, ax = plt.subplots(figsize=(8.2, 4.5))
    ax.bar(
        [ETIQUETAS[x] for x in orden],
        medias,
        yerr=errores,
        capsize=5,
        color=[COLORES[x] for x in orden],
    )
    ax.set_ylabel("Tiempo promedio de espera (minutos)")
    ax.set_title("Espera promedio por configuración")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    fig.savefig(FIGURAS / "espera_escenarios.png")
    plt.close(fig)

    por_accion = (
        clientes.groupby(["escenario", "accion"])["tiempo_espera"]
        .mean()
        .unstack()
        .reindex(orden)
    )
    fig, ax = plt.subplots(figsize=(8.2, 4.5))
    x = np.arange(len(orden))
    ancho = 0.36
    ax.bar(x - ancho / 2, por_accion["retiro"], ancho, label="Retiro", color="#08628b")
    ax.bar(x + ancho / 2, por_accion["pago"], ancho, label="Pago", color="#c82332")
    ax.set_xticks(x, [ETIQUETAS[v] for v in orden], rotation=15)
    ax.set_ylabel("Tiempo promedio de espera (minutos)")
    ax.set_title("La espera cambia según el tipo de operación")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURAS / "espera_por_accion.png")
    plt.close(fig)

    utilizacion = (
        cajeros.groupby(["escenario", "cajero"])["utilizacion"]
        .mean()
        .reset_index()
    )
    fig, axes = plt.subplots(2, 2, figsize=(8.2, 6.3), sharey=True)
    for ax, escenario in zip(axes.flat, orden):
        datos = utilizacion[utilizacion["escenario"] == escenario]
        ax.bar(datos["cajero"], 100 * datos["utilizacion"], color=COLORES[escenario])
        ax.axhline(80, color="#c82332", linestyle="--", linewidth=1, label="Referencia 80 %")
        ax.set_title(ETIQUETAS[escenario])
        ax.set_ylabel("Utilización (%)")
        ax.set_ylim(0, 100)
    fig.suptitle("Utilización promedio de cada cajero")
    fig.tight_layout()
    fig.savefig(FIGURAS / "utilizacion_cajeros.png")
    plt.close(fig)


if __name__ == "__main__":
    try:
        cantidad = int(sys.argv[1]) if len(sys.argv) > 1 else 100
        ejecutar(replicas=cantidad)
    except ValueError as error:
        raise SystemExit(f"Número de réplicas inválido: {error}") from error
