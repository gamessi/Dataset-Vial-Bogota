import os
import matplotlib.pyplot as plt
import seaborn as sns


""" paleta de colores para reportes visuales """
COLOR_FONDO = "#0D1117"
COLOR_TARJETA = "#161B22"
COLOR_BORDE = "#30363D"

COLOR_AZUL = "#2F81F7"
COLOR_AZUL_CLARO = "#79C0FF"
COLOR_VERDE = "#3FB950"
COLOR_ROJO = "#F85149"
COLOR_AMARILLO = "#D29922"
COLOR_NEUTRO = "#8B949E"
COLOR_BARRAS_DEFECTO = "#58A6FF"
COLOR_TEXTO = "#F0F6FC"
COLOR_TEXTO_OSCURO = "#24292F"

""" configuracion de estilo base """
sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.family"] = "sans-serif"


""" ajusta el grafico y lo guarda con alta resolucion """
def guardar(nombre_archivo, carpeta):
    os.makedirs(carpeta, exist_ok=True)
    plt.tight_layout()
    plt.savefig(
        os.path.join(carpeta, nombre_archivo),
        dpi=200,
        bbox_inches="tight"
    )
    plt.close()

""" aplica titulos jerarquicos y limpia bordes para mejorar lectura """
def estilizar_grafico(ax, titulo, subtitulo=None, xlabel=None, ylabel=None):
    if subtitulo:
        ax.set_title(f"{titulo}\n", fontsize=13, fontweight="bold", pad=14, loc="left", color=COLOR_TEXTO_OSCURO)
        ax.text(0, 1.02, subtitulo, transform=ax.transAxes, fontsize=10, color="#57606A", ha="left")
    else:
        ax.set_title(titulo, fontsize=13, fontweight="bold", pad=12, loc="left", color=COLOR_TEXTO_OSCURO)

    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, fontweight="bold", labelpad=8, color=COLOR_TEXTO_OSCURO)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, fontweight="bold", labelpad=8, color=COLOR_TEXTO_OSCURO)

    ax.grid(axis="x" if ax.get_ylabel() else "y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#D0D7DE")
    ax.spines["bottom"].set_color("#D0D7DE")

""" agrega valores exactos en cada barra para lectura directa """
def agregar_etiquetas_barras(ax, es_horizontal=False, formato="{:,}", sufijo="", padding=5, decimales=0):
    for contenedor in ax.containers:
        for barra in contenedor:
            if es_horizontal:
                ancho = barra.get_width()
                if ancho == 0 or (ancho != ancho):
                    continue
                texto = f"{ancho:,.{decimales}f}{sufijo}" if decimales > 0 else f"{int(round(ancho)):,}{sufijo}"
                ax.annotate(
                    texto,
                    xy=(ancho, barra.get_y() + barra.get_height() / 2),
                    xytext=(padding, 0),
                    textcoords="offset points",
                    ha="left",
                    va="center",
                    fontsize=9,
                    fontweight="bold",
                    color=COLOR_TEXTO_OSCURO
                )
            else:
                alto = barra.get_height()
                if alto == 0 or (alto != alto):
                    continue
                texto = f"{alto:,.{decimales}f}{sufijo}" if decimales > 0 else f"{int(round(alto)):,}{sufijo}"
                ax.annotate(
                    texto,
                    xy=(barra.get_x() + barra.get_width() / 2, alto),
                    xytext=(0, padding),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold",
                    color=COLOR_TEXTO_OSCURO
                )

""" genera dashboard de metricas """
def generar_tarjetas(metricas, carpeta):
    total_acc = metricas["accidentes"]
    total_veh = metricas["vehiculos"]

    fig, axes = plt.subplots(
        2,
        4,
        figsize=(18, 7.5),
        facecolor=COLOR_FONDO
    )

    tarjetas = [
        # fila 1
        (
            "TOTAL DE SINIESTROS",
            f"{metricas['accidentes']:,}",
            COLOR_AZUL,
            "100% registros consolidados"
        ),
        (
            "PERSONAS AFECTADAS",
            f"{metricas['personas']:,}",
            COLOR_VERDE,
            f"{metricas['heridos']:,} heridos / {metricas['fallecidos']:,} fallecidos"
        ),
        (
            "VEHÍCULOS EN SINIESTROS",
            f"{metricas['vehiculos']:,}",
            "#A371F7",
            "unidades totales en evento"
        ),
        (
            "SINIESTROS CON HERIDOS",
            f"{metricas['con_heridos']:,}",
            COLOR_AMARILLO,
            f"{(metricas['con_heridos']/total_acc*100):.1f}% de siniestros con lesiones"
        ),
        # fila 2
        (
            "SINIESTROS CON MUERTOS",
            f"{metricas['con_muertos']:,}",
            COLOR_ROJO,
            f"{(metricas['con_muertos']/total_acc*100):.1f}% tasa de letalidad"
        ),
        (
            "SOLO DAÑOS MATERIALES",
            f"{metricas['solo_danos']:,}",
            COLOR_AZUL_CLARO,
            f"{(metricas['solo_danos']/total_acc*100):.1f}% siniestros no lesivos"
        ),
        (
            "SERVICIO PARTICULAR",
            f"{metricas['particulares']:,}",
            "#56D364",
            f"{(metricas['particulares']/total_veh*100):.1f}% del total vehicular"
        ),
        (
            "SERVICIO PÚBLICO",
            f"{metricas['publicos']:,}",
            "#FF7B72",
            f"{(metricas['publicos']/total_veh*100):.1f}% del total vehicular"
        ),
    ]

    for ax, (titulo, valor, color, subtitulo) in zip(axes.flatten(), tarjetas):
        """ fondo y contorno de tarjeta """
        ax.set_facecolor(COLOR_TARJETA)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(COLOR_BORDE)
            spine.set_linewidth(1.2)

        """ franja de color indicadora """
        ax.plot(
            [0, 1],
            [1, 1],
            transform=ax.transAxes,
            color=color,
            linewidth=6,
            solid_capstyle="butt"
        )

        """ texto de categoria """
        ax.text(
            0.08,
            0.78,
            titulo,
            ha="left",
            va="center",
            fontsize=8.8,
            fontweight="bold",
            color="#8B949E",
            transform=ax.transAxes
        )

        """ valor de metrica principal """
        ax.text(
            0.08,
            0.48,
            valor,
            ha="left",
            va="center",
            fontsize=21,
            fontweight="bold",
            color=COLOR_TEXTO,
            transform=ax.transAxes
        )

        """ texto complementario inferior """
        ax.text(
            0.08,
            0.20,
            subtitulo,
            ha="left",
            va="center",
            fontsize=8.2,
            color="#7D8590",
            transform=ax.transAxes
        )

        """ punto de acento """
        ax.scatter(
            0.90,
            0.80,
            s=45,
            color=color,
            transform=ax.transAxes
        )

        ax.set_xticks([])
        ax.set_yticks([])

    """ titulo superior del tablero """
    fig.suptitle(
        "TABLERO EJECUTIVO DE SINIESTRALIDAD VIAL - BOGOTÁ D.C.",
        fontsize=16,
        fontweight="bold",
        color=COLOR_TEXTO,
        y=0.98
    )

    plt.subplots_adjust(
        left=0.03,
        right=0.97,
        top=0.90,
        bottom=0.06,
        hspace=0.25,
        wspace=0.10
    )

    os.makedirs(carpeta, exist_ok=True)
    plt.savefig(
        os.path.join(carpeta, "tarjetas_metricas.png"),
        dpi=200,
        bbox_inches="tight",
        facecolor=COLOR_FONDO
    )
    plt.close()



