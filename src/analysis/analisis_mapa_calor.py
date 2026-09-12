import re
import unicodedata

import geopandas as gpd
from matplotlib.pylab import norm
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

from src.graficos import guardar
from src.config import RUTA_GEOJSON_LOCALIDADES

COLUMNA_NOMBRE_GEOJSON = "Nombre de la localidad"

""" posiciones y llamadas para evitar colision en localidades centrales densas """
AJUSTES_POSICION = {
    "CANDELARIA": (-73.97, 4.595, True),
    "SANTA FE": (-73.97, 4.628, True),
    "LOS MARTIRES": (-74.15, 4.605, True),
    "ANTONIO NARINO": (-74.01, 4.575, True),
    "TEUSAQUILLO": (-74.15, 4.640, True),
    "BARRIOS UNIDOS": (-74.15, 4.670, True),
    "TUNJUELITO": (-74.17, 4.565, True),
    "RAFAEL URIBE URIBE": (-74.03, 4.545, True),
    "PUENTE ARANDA": (-74.108, 4.617, False),
}

""" normaliza nombres del geojson y dataset eliminando tildes y prefijos """
def _normalizar(texto):
    if not isinstance(texto, str):
        return texto
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
    limpio = sin_tildes.upper().strip()
    limpio = re.sub(r"^LA\s+", "", limpio)
    return limpio

""" procesa cruce espacial excluyendo sumapaz y genera mapa """
def analizar(siniestros, carpeta):
    conclusiones = []

    conteo = siniestros["CODIGO_LOCALIDAD_DESC"].value_counts().reset_index()
    conteo.columns = ["localidad_norm", "accidentes"]
    conteo["localidad_norm"] = conteo["localidad_norm"].map(_normalizar)

    localidades = gpd.read_file(RUTA_GEOJSON_LOCALIDADES)
    localidades["localidad_norm"] = localidades[COLUMNA_NOMBRE_GEOJSON].map(_normalizar)

    """ exclusion de sumapaz por no pertenecer al analisis """
    localidades = localidades[localidades["localidad_norm"] != "SUMAPAZ"].copy()

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

""" renderiza mapa  """
def _graficar_mapa(mapa, carpeta):
    fig, ax = plt.subplots(1, 1, figsize=(13, 14))
    mapa.plot(
        column="accidentes",
        cmap="YlOrRd",
        linewidth=1.0,
        edgecolor="#30363D",
        ax=ax,
        legend=True,
        legend_kwds={
            "label": "Número acumulado de accidentes",
            "shrink": 0.48,
            "orientation": "horizontal",
            "pad": 0.03
        },
    )

    """ titulo y subtitulo explicativo con margen adecuado """
    ax.set_title("MAPA DE CALOR: CONCENTRACIÓN DE SINIESTROS POR LOCALIDAD\n", fontsize=14, fontweight="bold", pad=15, color="#24292F", loc="center")
    ax.text(0.5, 0.985, "Zonas en tonos oscuros presentan mayor densidad de siniestros", transform=ax.transAxes, fontsize=10.5, color="#57606A", ha="center")

    _agregar_etiquetas(mapa, ax)

    guardar("mapa_calor_localidades.png", carpeta)


def _agregar_etiquetas(mapa, ax):
    for _, fila in mapa.iterrows():
        punto = fila.geometry.representative_point()
        num_casos = int(fila["accidentes"])
        nombre = fila[COLUMNA_NOMBRE_GEOJSON].title()
        etiqueta = f"{nombre}\n{num_casos:,}" if num_casos > 0 else nombre

    if norm in AJUSTES_POSICION:
            target_x, target_y, use_arrow = AJUSTES_POSICION[norm]
            if use_arrow:
                ax.annotate(
                    etiqueta,
                    xy=(punto.x, punto.y),
                    xytext=(target_x, target_y),
                    fontsize=8.2,
                    fontweight="bold",
                    ha="center",
                    va="center",
                    color="#0D1117",
                    arrowprops=dict(arrowstyle="->", color="#30363D", lw=1.2, shrinkB=4),
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="#F6F8FA", edgecolor="#D0D7DE", alpha=0.92, lw=0.8)
                )
            else:
                texto = ax.text(target_x, target_y, etiqueta, fontsize=8.2, fontweight="bold", ha="center", va="center", color="#0D1117")
                texto.set_path_effects([path_effects.Stroke(linewidth=3.0, foreground="white"), path_effects.Normal()])
    else:
            texto = ax.text(
                punto.x,
                punto.y,
                etiqueta,
                fontsize=8.5,
                fontweight="bold",
                ha="center",
                va="center",
                color="#0D1117",
            )
            texto.set_path_effects([
                path_effects.Stroke(linewidth=3.0, foreground="white"),
                path_effects.Normal()
            ])     