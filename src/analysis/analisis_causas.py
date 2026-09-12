""" analisis de causas frecuentes de siniestros viales """

import matplotlib.pyplot as plt
from src.graficos import (
    guardar,
    estilizar_grafico,
    COLOR_VERDE,
    COLOR_ROJO
)


def analizar(hipotesis, carpeta):
    """ genera visualizacion didactica del top de causas de accidentes """
    top_causas = hipotesis["CAUSA_DESC"].value_counts().head(10)
    total_hipotesis = len(hipotesis)

    fig, ax = plt.subplots(figsize=(11.5, 6.5))

    """ resalta la causa principal en color diferenciado """
    colores = [COLOR_ROJO if i == 0 else COLOR_VERDE for i in range(len(top_causas))]
    barras = ax.barh(top_causas.index, top_causas.values, color=colores, height=0.65)
    ax.invert_yaxis()

    """ margen derecho amplio para evitar solapamiento """
    ax.set_xlim(0, top_causas.max() * 1.25)

    """ etiquetas de conteo y porcentaje para cada causa """
    for barra in barras:
        ancho = barra.get_width()
        porc = (ancho / total_hipotesis) * 100
        ax.annotate(
            f" {int(ancho):,} ({porc:.1f}%)",
            xy=(ancho, barra.get_y() + barra.get_height() / 2),
            va="center",
            ha="left",
            fontsize=9,
            fontweight="bold",
            color="#24292F"
        )

    subtitulo = f"Causa principal: '{top_causas.index[0]}' representa {top_causas.iloc[0]:,} siniestros ({top_causas.iloc[0]/total_hipotesis*100:.1f}%)"
    estilizar_grafico(ax, "Top 10 Causas Hipotéticas de Siniestros Viales", subtitulo=subtitulo, xlabel="Número de casos reportados")

    guardar("top_causas.png", carpeta)

    conclusion = (
        f"La causa más frecuente de siniestros es '{top_causas.index[0]}', presente en "
        f"{top_causas.iloc[0]:,} registros de hipoteticos accidentes."
    )
    return [conclusion]


