""" analisis del tipo de servicio del vehiculo: particular, publico, oficial, diplomatico """
import matplotlib.pyplot as plt
from src.graficos import guardar, COLOR_VERDE, COLOR_ROJO
from src.config import MIN_ACCIDENTES_PARA_TASA


def analizar(vehiculos, carpeta):
    conclusiones = []

    por_servicio = vehiculos["SERVICIO_DESC"].value_counts()
    conclusiones.append(
        f"El {por_servicio.iloc[0] / por_servicio.sum() * 100:.1f}% de los vehículos involucrados "
        f"en siniestros son de servicio '{por_servicio.index[0]}' ({por_servicio.iloc[0]:,} casos)."
    )

    conclusiones.append(_tasa_fuga_por_servicio(vehiculos, por_servicio, carpeta))

    plt.figure(figsize=(9, 5))
    por_servicio.plot(
    kind="bar",
    color=COLOR_VERDE)
    plt.title("Vehículos involucrados en siniestros por tipo de servicio")
    plt.xlabel("Tipo de servicio")
    plt.ylabel("Número de vehículos")
    plt.xticks(rotation=0)
    guardar("top_servicio.png", carpeta)

    return conclusiones


def _tasa_fuga_por_servicio(vehiculos, por_servicio, carpeta):
    # Igual que con las localidades: solo se consideran tipos de servicio con muestra
    # suficiente. 'Diplomatico' tiene muy pocos casos y una sola fuga distorsionaría la tasa.
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


def _graficar_tasa_fuga(tasa, carpeta):
    plt.figure(figsize=(9, 5))
    tasa.plot(
    kind="bar",
    color=COLOR_ROJO)
    plt.title("Tasa de fuga tras el siniestro, por tipo de servicio")
    plt.xlabel("Tipo de servicio")
    plt.ylabel("% de vehículos que huyeron")
    plt.xticks(rotation=0)
    guardar("tasa_fuga_servicio.png", carpeta)