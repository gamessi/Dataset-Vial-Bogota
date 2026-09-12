import matplotlib.pyplot as plt
from src.graficos import guardar

""" procesa tipos de vehiculos y genera grafica """
def analizar(vehiculos, carpeta):
    conteo = vehiculos["CLASE_DESC"].value_counts()
    total_vehiculos = len(vehiculos)

    top6 = conteo.head(6)
    otros = conteo.iloc[6:].sum()

    top_clase = top6.copy()
    if otros > 0:
        top_clase["Otros"] = otros

    colores = ["#2F81F7", "#3FB950", "#F85149", "#D29922", "#A371F7", "#56D364", "#8B949E"][:len(top_clase)]

    fig, ax = plt.subplots(figsize=(11, 6.5))

    """ genera grafico con etiquetas formateadas y espacio despejado """
    etiquetas_leyenda = [f"{k}: {v:,} ({v/total_vehiculos*100:.1f}%)" for k, v in top_clase.items()]

    wedges, texts, autotexts = ax.pie(
        top_clase,
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.76,
        colors=colores,
        wedgeprops=dict(width=0.40, edgecolor="white", linewidth=2.5),
    )

    plt.setp(autotexts, size=9, weight="bold", color="white")

    """ cuadro de leyenda lateral para evitar mezclar texto sobre sectores """
    ax.legend(
        wedges,
        etiquetas_leyenda,
        title="Tipos de Vehículo",
        title_fontsize=10.5,
        loc="center left",
        bbox_to_anchor=(0.95, 0.5),
        frameon=True,
        facecolor="white",
        edgecolor="#D0D7DE",
        fontsize=9.5
    )

    """ texto central con total acumulado """
    ax.text(
        0,
        0,
        f"TOTAL\n{total_vehiculos:,}\nvehículos",
        ha="center",
        va="center",
        fontsize=11.5,
        fontweight="bold",
        color="#24292F"
    )

    top1 = top6.index[0]
    top2 = top6.index[1]
    ax.set_title("DISTRIBUCIÓN DE TIPOS DE VEHÍCULO INVOLUCRADOS\n", fontsize=13.5, fontweight="bold", pad=14, color="#24292F", loc="center")
    fig.text(0.5, 0.94, f"'{top1}' y '{top2}' concentran la gran mayoría de incidentes en la ciudad", fontsize=10, color="#57606A", ha="center")
    ax.axis("equal")

    guardar("top_vehiculos.png", carpeta)
    plt.close(fig)

    conclusion = (
        f"El tipo de vehículo más involucrado en siniestros es "
        f"'{top6.index[0]}' ({top6.iloc[0]:,} casos), seguido de "
        f"'{top6.index[1]}' ({top6.iloc[1]:,} casos). "
    )

    return [conclusion]

