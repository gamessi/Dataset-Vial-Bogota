# Análisis geográfico: qué localidades concentran más siniestros y cuáles son más letales
import matplotlib.pyplot as plt
from src.graficos import guardar
from src.config import MIN_ACCIDENTES_PARA_TASA


def analizar(siniestros, carpeta):
    conclusiones = []

    por_localidad = siniestros["CODIGO_LOCALIDAD_DESC"].value_counts()
    top = por_localidad.index[0]
    conclusiones.append(
        f"La localidad con más siniestros es '{top}', con {por_localidad.iloc[0]:,} "
        f"accidentes registrados en el periodo ({por_localidad.iloc[0] / len(siniestros) * 100:.1f}% del total)."
    )

    conclusiones.append(_localidad_mas_letal(siniestros, por_localidad))

    plt.figure(figsize=(9, 7))
    por_localidad.head(10).plot(kind="barh", color="darkorange")
    plt.title("Top 10 localidades con más siniestros")
    plt.xlabel("Número de accidentes")
    plt.gca().invert_yaxis()
    guardar("top_localidades.png", carpeta)

    return conclusiones


def _localidad_mas_letal(siniestros, por_localidad):
    # Solo se consideran localidades con muestra suficiente: con varios accidentes totales
    # Sumapaz tiene 7 accidentes en 6 años, un solo caso puede disparar la tasa a 30-40% de forma engañosa.
    con_muestra_suficiente = por_localidad[por_localidad >= MIN_ACCIDENTES_PARA_TASA].index

    fatales_por_loc = siniestros[siniestros["GRAVEDAD_DESC"] == "Con Muertos"]["CODIGO_LOCALIDAD_DESC"].value_counts()
    tasa = (fatales_por_loc / por_localidad * 100).dropna()
    tasa = tasa[tasa.index.isin(con_muestra_suficiente)].sort_values(ascending=False)

    return (
        f"Entre localidades con al menos {MIN_ACCIDENTES_PARA_TASA} accidentes registrados, "
        f"'{tasa.index[0]}' tiene la mayor proporción de accidentes con muertos respecto a su total "
        f"{tasa.iloc[0]:.2f}% de sus accidentes son fatales."
    )
