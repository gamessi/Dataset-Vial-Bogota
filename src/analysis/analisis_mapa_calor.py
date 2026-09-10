""" analisis_mapa_calor.py — mapa coroplético de accidentes por localidad """
import re
import unicodedata
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import geopandas as gpd

import matplotlib.pyplot as plt

try:
    import geopandas as gpd
except ImportError:  # pragma: no cover - dependency optional at analysis time
    gpd = None

from src.graficos import guardar
from src.config import RUTA_GEOJSON_LOCALIDADES

COLUMNA_NOMBRE_GEOJSON = "Nombre de la localidad"


def _normalizar(texto):
    """Normaliza nombres de localidad para poder cruzar el dataset con el geojson:
    sin tildes, en mayúsculas, sin espacios sobrantes y sin el artículo 'LA ' inicial
    (el dataset suele decir 'La Candelaria' mientras el geojson solo dice 'Candelaria')."""
    if not isinstance(texto, str):
        return texto
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
    limpio = sin_tildes.upper().strip()
    limpio = re.sub(r"^LA\s+", "", limpio)
    return limpio


def analizar(siniestros, carpeta):
    conclusiones = []

    conteo = siniestros["CODIGO_LOCALIDAD_DESC"].value_counts().reset_index()
    conteo.columns = ["localidad_norm", "accidentes"]
    conteo["localidad_norm"] = conteo["localidad_norm"].map(_normalizar)

    localidades = gpd.read_file(RUTA_GEOJSON_LOCALIDADES)
    localidades["localidad_norm"] = localidades[COLUMNA_NOMBRE_GEOJSON].map(_normalizar)

    mapa = localidades.merge(conteo, on="localidad_norm", how="left")
    mapa["accidentes"] = mapa["accidentes"].fillna(0)

    sin_match = mapa[mapa["accidentes"] == 0][COLUMNA_NOMBRE_GEOJSON].tolist()
    if sin_match:
        print(f"Aviso: localidades del geojson sin datos cruzados: {sin_match}")

    _graficar_mapa(mapa, carpeta)

    top_geo = mapa.sort_values("accidentes", ascending=False).iloc[0]
    conclusiones.append(
        f"En el mapa por localidad, '{top_geo[COLUMNA_NOMBRE_GEOJSON].title()}' concentra la mayor "
        f"cantidad de siniestros con {int(top_geo['accidentes']):,} casos."
    )
    return conclusiones


def _graficar_mapa(mapa, carpeta):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    mapa.plot(
        column="accidentes",
        cmap="OrRd",
        linewidth=0.8,
        edgecolor="0.8",
        ax=ax,
        legend=True,
        legend_kwds={"label": "Número de accidentes", "shrink": 0.6},
    )
    ax.set_title("Accidentes de tránsito por localidad — Bogotá", fontsize=14, fontweight="bold")
    ax.axis("off")
    guardar("mapa_calor_localidades.png", carpeta)