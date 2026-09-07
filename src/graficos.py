"""Utilidades compartidas para generar gráficos y tarjetas."""

import os

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def guardar(nombre_archivo, carpeta):
    """Ajusta el layout y guarda la figura actual de matplotlib."""

    os.makedirs(carpeta, exist_ok=True)

    plt.tight_layout()
    plt.savefig(
        os.path.join(carpeta, nombre_archivo),
        dpi=150,
        bbox_inches="tight"
    )
    plt.close()


def generar_tarjetas(metricas, carpeta):
    """Genera una imagen con tarjetas de indicadores principales."""

    fig, axes = plt.subplots(1, 5, figsize=(16, 3.5))

    tarjetas = [
        (
            "TOTAL DE\nACCIDENTES",
            f"{metricas['accidentes']:,}"
        ),
        (
            "PERSONAS\nINVOLUCRADAS",
            f"{metricas['personas']:,}"
        ),
        (
            "VEHÍCULOS\nINVOLUCRADOS",
            f"{metricas['vehiculos']:,}"
        ),
        (
            "FECHA\nINICIAL",
            metricas["fecha_inicio"].strftime("%d/%m/%Y")
        ),
        (
            "FECHA\nFINAL",
            metricas["fecha_fin"].strftime("%d/%m/%Y")
        ),
    ]

    for ax, (titulo, valor) in zip(axes, tarjetas):

        ax.set_facecolor("white")

        # Borde de la tarjeta
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(1.5)

        # Título
        ax.text(
            0.5,
            0.72,
            titulo,
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            transform=ax.transAxes
        )

        # Valor principal
        ax.text(
            0.5,
            0.38,
            valor,
            ha="center",
            va="center",
            fontsize=20,
            fontweight="bold",
            transform=ax.transAxes
        )

        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle(
        "Dashboard - Siniestros Viales Bogotá D.C.",
        fontsize=16,
        fontweight="bold",
        y=1.05
    )

    guardar("tarjetas_metricas.png", carpeta)