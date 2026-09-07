""" (hipótesis) de las causas mas frecuentes de los siniestros."""

import matplotlib.pyplot as plt
from src.graficos import guardar, COLOR_VERDE


def analizar(hipotesis, carpeta):
    top_causas = hipotesis["CAUSA_DESC"].value_counts().head(10)

    plt.figure(figsize=(10, 7))
    top_causas.plot(
    kind="barh",
    color=COLOR_VERDE)
    plt.title("Top 10 causas más frecuentes de siniestros")
    plt.xlabel("Número de casos")
    plt.gca().invert_yaxis()
    guardar("top_causas.png", carpeta)

    conclusion = (
        f"La causa más frecuente de siniestros es '{top_causas.index[0]}', presente en "
        f"{top_causas.iloc[0]:,} registros de hipoteticos accidentes."
    )
    return [conclusion]
