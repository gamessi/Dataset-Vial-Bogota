""" analisis geografico: concentracion de siniestros y letalidad por localidad """

import matplotlib.pyplot as plt
from src.graficos import (
    guardar,
    estilizar_grafico,
    agregar_etiquetas_barras,
    COLOR_AZUL,
    COLOR_ROJO
)
from src.config import MIN_ACCIDENTES_PARA_TASA


def analizar(siniestros, carpeta):
    """ procesa analisis de siniestros por localidad y genera graficos didacticos """
    conclusiones = []

    por_localidad = siniestros["CODIGO_LOCALIDAD_DESC"].value_counts()
    top = por_localidad.index[0]
    total_siniestros = len(siniestros)
    porc_top = (por_localidad.iloc[0] / total_siniestros) * 100

    conclusiones.append(
        f"La localidad con más siniestros es '{top}', con {por_localidad.iloc[0]:,} "
        f"accidentes, ({porc_top:.1f}% del total)."
    )

    conclusiones.append(_localidad_mas_letal(siniestros, por_localidad))

    top10 = por_localidad.head(10)
    fig, ax = plt.subplots(figsize=(11, 6.5))

    """ resalta la localidad numero uno en color critico """
    colores = [COLOR_ROJO if loc == top else COLOR_AZUL for loc in top10.index]
    barras = ax.barh(top10.index, top10.values, color=colores, height=0.65)
    ax.invert_yaxis()

    """ margen derecho amplio para evitar corte de texto """
    ax.set_xlim(0, top10.max() * 1.22)

    """ agrega etiquetas con conteo y porcentaje relativo sobre el total """
    for barra in barras:
        ancho = barra.get_width()
        porc = (ancho / total_siniestros) * 100
        ax.annotate(
            f" {int(ancho):,} ({porc:.1f}%)",
            xy=(ancho, barra.get_y() + barra.get_height() / 2),
            va="center",
            ha="left",
            fontsize=9,
            fontweight="bold",
            color="#24292F"
        )

    subtitulo = f"{top} encabeza con {top10.iloc[0]:,} casos ({porc_top:.1f}% de la ciudad)"
    estilizar_grafico(ax, "Top 10 Localidades con Mayor Número de Siniestros", subtitulo=subtitulo, xlabel="Número total de accidentes")

    guardar("top_localidades.png", carpeta)

    return conclusiones


def _localidad_mas_letal(siniestros, por_localidad):
    """ calcula la localidad con mayor proporcion de fallecidos """
    con_muestra_suficiente = por_localidad[por_localidad >= MIN_ACCIDENTES_PARA_TASA].index

    fatales_por_loc = siniestros[siniestros["GRAVEDAD_DESC"] == "Con Muertos"]["CODIGO_LOCALIDAD_DESC"].value_counts()
    tasa = (fatales_por_loc / por_localidad * 100).dropna()
    tasa = tasa[tasa.index.isin(con_muestra_suficiente)].sort_values(ascending=False)

    return (
        f"Entre localidades con al menos {MIN_ACCIDENTES_PARA_TASA} accidentes registrados, "
        f"'{tasa.index[0]}' tiene la mayor proporción de accidentes con muertos respecto a su total "
        f"{tasa.iloc[0]:.2f}% de sus accidentes son fatales."
    )


