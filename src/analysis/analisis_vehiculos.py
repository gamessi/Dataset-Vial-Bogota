import matplotlib.pyplot as plt
from src.graficos import guardar


def analizar(vehiculos, carpeta):

    conteo = vehiculos["CLASE_DESC"].value_counts()

    top6 = conteo.head(6)
    otros = conteo.iloc[6:].sum()

    top_clase = top6.copy()
    if otros > 0:
        top_clase["Otros"] = otros

    # Gráfico de dona
    fig, ax = plt.subplots(figsize=(10, 7))

    wedges, texts, autotexts = ax.pie(
        top_clase,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.78,
        wedgeprops=dict(width=0.4, edgecolor="white"),
    )

    plt.setp(autotexts, size=9, weight="bold")

    ax.legend(
        wedges,
        top_clase.index,
        title="Tipos de Vehículo",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    ax.set_title("Distribución de los tipos de vehículo más involucrados", pad=20)
    ax.axis("equal")

    plt.tight_layout()
    guardar("top_vehiculos.png", carpeta)
    plt.close(fig)

    conclusion = (
        f"El tipo de vehículo más involucrado en siniestros es "
        f"'{top6.index[0]}' ({top6.iloc[0]:,} casos), seguido de "
        f"'{top6.index[1]}' ({top6.iloc[1]:,} casos). "
      )

    return [conclusion]