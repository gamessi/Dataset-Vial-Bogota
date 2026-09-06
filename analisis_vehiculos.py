"""Análisis de los tipos de vehículo más involucrados en siniestros."""
import matplotlib.pyplot as plt
from graficos import guardar


def analizar(vehiculos, carpeta):
    top_clase = vehiculos["CLASE_DESC"].value_counts().head(10)

    plt.figure(figsize=(10, 7))
    top_clase.plot(kind="barh", color="mediumpurple")
    plt.title("Top 10 tipos de vehículo involucrados en siniestros")
    plt.xlabel("Número de casos")
    plt.gca().invert_yaxis()
    guardar("top_vehiculos.png", carpeta)

    conclusion = (
        f"El tipo de vehículo más involucrado en siniestros es '{top_clase.index[0]}' "
        f"({top_clase.iloc[0]:,} casos), seguido de '{top_clase.index[1]}' ({top_clase.iloc[1]:,} casos)."
    )
    return [conclusion]
