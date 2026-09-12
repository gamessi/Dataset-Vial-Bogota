import matplotlib.pyplot as plt
from src.graficos import (
    guardar,
    estilizar_grafico,
    COLOR_VERDE,
    COLOR_ROJO,
    COLOR_AZUL
)
from src.config import MIN_ACCIDENTES_PARA_TASA

""" procesa analisis de tipo de servicio y comportamiento de fuga """
def analizar(vehiculos, carpeta):
    conclusiones = []

    por_servicio = vehiculos["SERVICIO_DESC"].value_counts()
    total = por_servicio.sum()
    porc_top = (por_servicio.iloc[0] / total) * 100

    conclusiones.append(
        f"El {porc_top:.1f}% de los vehículos involucrados "
        f"en siniestros son de servicio '{por_servicio.index[0]}' ({por_servicio.iloc[0]:,} casos)."
    )

    conclusiones.append(_tasa_fuga_por_servicio(vehiculos, por_servicio, carpeta))

    fig, ax = plt.subplots(figsize=(10.5, 5.8))

    """ margen vertical para etiquetas superiores """
    ax.set_ylim(0, por_servicio.max() * 1.20)

    """ resalta el servicio mayor """
    colores = [COLOR_AZUL if s == por_servicio.index[0] else COLOR_VERDE for s in por_servicio.index]
    barras = ax.bar(por_servicio.index, por_servicio.values, color=colores, width=0.58)

    """ anota valores exactos y participacion porcentual """
    for barra in barras:
        alto = barra.get_height()
        porc = (alto / total) * 100
        ax.annotate(
            f"{int(alto):,}\n({porc:.1f}%)",
            xy=(barra.get_x() + barra.get_width() / 2, alto),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="#24292F"
        )

    subtitulo = f"Servicio '{por_servicio.index[0]}' predomina con {por_servicio.iloc[0]:,} unidades ({porc_top:.1f}%)"
    estilizar_grafico(ax, "Vehículos Involucrados por Tipo de Servicio", subtitulo=subtitulo, xlabel="Tipo de servicio", ylabel="Número de vehículos")
    ax.tick_params(axis="x", rotation=0)

    guardar("top_servicio.png", carpeta)

    return conclusiones

""" calcula porcentaje de conductores que huyen segun el servicio """
def _tasa_fuga_por_servicio(vehiculos, por_servicio, carpeta):
    con_muestra_suficiente = por_servicio[por_servicio >= MIN_ACCIDENTES_PARA_TASA].index

    en_fuga = vehiculos[vehiculos["ENFUGA"] == "S"]["SERVICIO_DESC"].value_counts()
    tasa = (en_fuga / por_servicio * 100).dropna()
    tasa = tasa[tasa.index.isin(con_muestra_suficiente)].sort_values(ascending=False)

    _graficar_tasa_fuga(tasa, carpeta)

    return (
        f"Los vehículos de servicio '{tasa.index[0]}' tienen la mayor tasa de fuga tras el siniestro "
        f"({tasa.iloc[0]:.1f}%), muy por encima del resto de tipos de servicio "
        f"({tasa.iloc[1]:.1f}% en '{tasa.index[1]}')."
    )

""" grafica porcentaje de fuga  """
def _graficar_tasa_fuga(tasa, carpeta):
    fig, ax = plt.subplots(figsize=(10.5, 5.8))

    """ margen vertical para etiquetas superiores """
    ax.set_ylim(0, tasa.max() * 1.22)

    """ resalta el servicio con mayor porcentaje de fuga """
    colores = [COLOR_ROJO if i == 0 else "#E36209" if i == 1 else COLOR_AZUL for i in range(len(tasa))]
    barras = ax.bar(tasa.index, tasa.values, color=colores, width=0.52)

    """ anota tasa porcentual directa """
    for barra in barras:
        alto = barra.get_height()
        ax.annotate(
            f"{alto:.1f}%",
            xy=(barra.get_x() + barra.get_width() / 2, alto),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color="#24292F"
        )


    subtitulo = f"Servicio '{tasa.index[0]}' presenta la mayor tasa de evasión con {tasa.iloc[0]:.1f}% de vehículos en fuga"
    estilizar_grafico(ax, "Tasa de Fuga tras Siniestro según Tipo de Servicio", subtitulo=subtitulo, xlabel="Tipo de servicio", ylabel="% de vehículos que huyeron")
    ax.tick_params(axis="x", rotation=0)

    guardar("tasa_fuga_servicio.png", carpeta)
