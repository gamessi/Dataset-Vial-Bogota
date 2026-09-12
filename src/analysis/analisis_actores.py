""" analisis de actores viales: roles, demografia y vulnerabilidad """

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.graficos import (
    guardar,
    estilizar_grafico,
    COLOR_ROJO,
    COLOR_AZUL,
    COLOR_VERDE,
    COLOR_AMARILLO
)


def analizar(actores, carpeta):
    """ procesa datos de victimas y genera graficos didacticos de impacto """
    graves = actores[actores["ESTADO"].isin(["HERIDO", "MUERTO"])]

    conclusiones = [
        _condicion_mas_afectada(graves),
        _tasa_mortalidad_por_condicion(actores),
    ]

    sexo_conclusion = _mayoria_sexo_fallecidos(actores)
    if sexo_conclusion:
        conclusiones.append(sexo_conclusion)

    _graficar_actores_afectados(graves, carpeta)
    _graficar_distribucion_edad(graves, carpeta)

    return conclusiones


def _condicion_mas_afectada(graves):
    """ identifica el rol con mayor numero de personas afectadas """
    por_condicion = graves["CONDICION"].value_counts()
    return (
        f"Entre las personas heridas o fallecidas la condición más frecuente es "
        f"'{por_condicion.index[0].title()}' ({por_condicion.iloc[0]:,} casos), lo que indica el grupo más vulnerable en los siniestros.")


def _tasa_mortalidad_por_condicion(actores):
    """ calcula que condicion tiene la mayor letalidad relativa """
    muertos = actores[actores["ESTADO"] == "MUERTO"]["CONDICION"].value_counts()
    total = actores["CONDICION"].value_counts()
    tasa = (muertos / total * 100).dropna().sort_values(ascending=False)
    return (
        f"'{tasa.index[0].title()}' tiene la tasa de mortalidad más alta entre actores viales ({tasa.iloc[0]:.2f}%) de los registros de esa condición terminan en muerte.")


def _mayoria_sexo_fallecidos(actores):
    """ determina si existe concentracion de genero en fallecidos """
    muertos_sexo = actores[actores["ESTADO"] == "MUERTO"]["SEXO"].value_counts()
    if len(muertos_sexo) == 0:
        return None
    proporcion = muertos_sexo.iloc[0] / muertos_sexo.sum()
    if proporcion <= 0.5:
        return None
    return (
        f"El {proporcion * 100:.1f}% de las víctimas mortales son de sexo "
        f"'{muertos_sexo.index[0].lower()}'.")


def _graficar_actores_afectados(graves, carpeta):
    """ genera grafico didactico de actores viales heridos o fallecidos """
    conteo = graves["CONDICION"].value_counts()
    total = conteo.sum()
    top = conteo.index[0]

    fig, ax = plt.subplots(figsize=(10.5, 5.8))

    """ margen vertical amplio para etiquetas """
    ax.set_ylim(0, conteo.max() * 1.20)

    """ resalta el actor mas vulnerable """
    colores = [COLOR_ROJO if c == top else COLOR_AZUL for c in conteo.index]
    barras = ax.bar(conteo.index, conteo.values, color=colores, width=0.62)

    """ agrega etiquetas con conteo y porcentaje relativo """
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

    subtitulo = f"{top.title()} es el rol más afectado concentrando {conteo.iloc[0]:,} personas ({conteo.iloc[0]/total*100:.1f}%)"
    estilizar_grafico(ax, "Personas Heridas o Fallecidas según Condición en el Siniestro", subtitulo=subtitulo, xlabel="Condición / Rol", ylabel="Número de personas")

    guardar("actores_afectados.png", carpeta)



def _graficar_distribucion_edad(graves, carpeta):
    """ genera histograma didactico con mediana y rango critico de edad """
    graves = graves.copy()
    graves["EDAD"] = pd.to_numeric(graves["EDAD"], errors="coerce")
    edades_validas = graves[(graves["EDAD"] > 0) & (graves["EDAD"] < 100)]
    mediana = edades_validas["EDAD"].median()

    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.histplot(
        edades_validas["EDAD"],
        bins=30,
        kde=True,
        color=COLOR_VERDE,
        ax=ax,
        edgecolor="white",
        alpha=0.7
    )

    """ linea indicadora de mediana de edad """
    ax.axvline(mediana, color=COLOR_ROJO, linestyle="--", linewidth=2, label=f"Mediana: {int(mediana)} años")
    ax.annotate(
        f"Edad central: {int(mediana)} años",
        xy=(mediana, ax.get_ylim()[1] * 0.85),
        xytext=(15, 0),
        textcoords="offset points",
        fontsize=9.5,
        fontweight="bold",
        color=COLOR_ROJO,
        arrowprops=dict(arrowstyle="->", color=COLOR_ROJO, lw=1.2)
    )

    subtitulo = f"Alta concentración de víctimas en población joven y económicamente activa (mediana {int(mediana)} años)"
    estilizar_grafico(ax, "Distribución de Edad de Heridos y Fallecidos", subtitulo=subtitulo, xlabel="Edad (años)", ylabel="Número de víctimas")
    ax.legend(frameon=True, facecolor="white", edgecolor="#D0D7DE")

    guardar("distribucion_edad.png", carpeta)

