""" utilidades compartidas para generar y guardar graficos """

import os

import matplotlib.pyplot as plt
import seaborn as sns


# paleta de colores
COLOR_FONDO = "#0D1117"
COLOR_TARJETA = "#161B22"
COLOR_BORDE = "#30363D"

COLOR_AZUL = "#58A6FF"
COLOR_VERDE = "#3FB950"
COLOR_ROJO = "#F85149"

COLOR_TEXTO = "#F0F6FC"

sns.set_theme(style="whitegrid")


def guardar(nombre_archivo, carpeta):
    """ ajusta el grafico y lo guarda en la carpeta de salida """

    os.makedirs(carpeta, exist_ok=True)

    plt.tight_layout()

    plt.savefig(
        os.path.join(carpeta, nombre_archivo),
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()


def generar_tarjetas(metricas, carpeta):
    """ genera las tarjetas con los indicadores principales """

    fig, axes = plt.subplots(
        1,
        5,
        figsize=(16, 3),
        facecolor=COLOR_FONDO
    )

    tarjetas = [
        (
            "TOTAL DE ACCIDENTES",
            f"{metricas['accidentes']:,}",
            COLOR_AZUL
        ),
        (
            "PERSONAS INVOLUCRADAS",
            f"{metricas['personas']:,}",
            COLOR_VERDE
        ),
        (
            "VEHÍCULOS INVOLUCRADOS",
            f"{metricas['vehiculos']:,}",
            COLOR_ROJO
        ),
        (
            "FECHA INICIAL",
            metricas["fecha_inicio"].strftime("%d/%m/%Y"),
            COLOR_AZUL
        ),
        (
            "FECHA FINAL",
            metricas["fecha_fin"].strftime("%d/%m/%Y"),
            COLOR_VERDE
        ),
    ]

    for ax, (titulo, valor, color) in zip(axes, tarjetas):

        # fondo de la tarjeta
        ax.set_facecolor(COLOR_TARJETA)

        # borde de la tarjeta
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(COLOR_BORDE)
            spine.set_linewidth(1.2)

        # linea superior de color
        ax.plot(
            [0, 1],
            [1, 1],
            transform=ax.transAxes,
            color=color,
            linewidth=5,
            solid_capstyle="butt"
        )

        # titulo
        ax.text(
            0.08,
            0.72,
            titulo,
            ha="left",
            va="center",
            fontsize=9,
            fontweight="bold",
            color="#8B949E",
            transform=ax.transAxes
        )

        # valor principal
        ax.text(
            0.08,
            0.42,
            valor,
            ha="left",
            va="center",
            fontsize=21,
            fontweight="bold",
            color=COLOR_TEXTO,
            transform=ax.transAxes
        )

        # indicador de color
        ax.scatter(
            0.91,
            0.82,
            s=45,
            color=color,
            transform=ax.transAxes
        )

        # eliminar ejes
        ax.set_xticks([])
        ax.set_yticks([])

    # titulo del dashboard
    fig.suptitle(
        "Dashboard",
        fontsize=18,
        fontweight="bold",
        color=COLOR_TEXTO,
        y=0.98
    )

    plt.subplots_adjust(
        left=0.02,
        right=0.98,
        top=0.78,
        bottom=0.08,
        wspace=0.06
    )

    os.makedirs(carpeta, exist_ok=True)

    plt.savefig(
        os.path.join(carpeta, "tarjetas_metricas.png"),
        dpi=150,
        bbox_inches="tight",
        facecolor=COLOR_FONDO
    )

    plt.close()

