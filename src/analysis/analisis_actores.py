# Análisis de las personas involucradas: rol, mortalidad, sexo y edad.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.graficos import guardar


def analizar(actores, carpeta):
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
    por_condicion = graves["CONDICION"].value_counts()
    return (
        f"Entre las personas heridas o fallecidas la condición más frecuente es "
        f"'{por_condicion.index[0].title()}' ({por_condicion.iloc[0]:,} casos), lo que indica el grupo más vulnerable en los siniestros.")


def _tasa_mortalidad_por_condicion(actores):
    muertos = actores[actores["ESTADO"] == "MUERTO"]["CONDICION"].value_counts()
    total = actores["CONDICION"].value_counts()
    tasa = (muertos / total * 100).dropna().sort_values(ascending=False)
    return (
        f"'{tasa.index[0].title()}' tiene la tasa de mortalidad más alta entre actores viales ({tasa.iloc[0]:.2f}%) de los registros de esa condición terminan en muerte.")


def _mayoria_sexo_fallecidos(actores):
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
    plt.figure(figsize=(9, 5))
    graves["CONDICION"].value_counts().plot(kind="bar", color="crimson")
    plt.title("Personas heridas o fallecidas por condición (rol) en el siniestro")
    plt.ylabel("Número de personas")
    guardar("actores_afectados.png", carpeta)


def _graficar_distribucion_edad(graves, carpeta):
    # EDAD viene con tipos mixtos (numero y NULL) en el data set, se fuerza a numérico.
    graves = graves.copy()
    graves["EDAD"] = pd.to_numeric(graves["EDAD"], errors="coerce")
    edades_validas = graves[(graves["EDAD"] > 0) & (graves["EDAD"] < 100)]

    plt.figure(figsize=(9, 5))
    sns.histplot(edades_validas["EDAD"], bins=30, kde=True, color="teal")
    plt.title("Distribución de edad de heridos y fallecidos")
    plt.xlabel("Edad")
    guardar("distribucion_edad.png", carpeta)
