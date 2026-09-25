import re
import matplotlib.pyplot as plt
from src.graficos import (
    guardar,
    estilizar_grafico,
    COLOR_AZUL,
    COLOR_ROJO
)

""" extrae el nombre base de la via eliminando el numero de cruce y sufijos """
def _extraer_corredor(direccion):
    if not isinstance(direccion, str):
        return None

    direccion = direccion.strip().upper()

    """ unifica variantes de avenida a 'AV' para evitar redundancia en el conteo """
    direccion = re.sub(r"^(AVENIDA|AVE|AV\.)\s+", "AV ", direccion)

    """ elimina palabra redundante cuando el dato trae 'AV AVENIDA ...' """
    direccion = re.sub(r"^AV\s+(AVENIDA|AVE|AV\.?)\s+", "AV ", direccion)

    """ elimina el tramo desde el simbolo # o la palabra SUR/NORTE/ESTE/OESTE en adelante """
    direccion = re.sub(r"\s*#.*$", "", direccion)
    direccion = re.sub(r"\s+(SUR|NORTE|ESTE|OESTE)\s*$", "", direccion)

    """ normaliza espacios multiples """
    direccion = re.sub(r"\s+", " ", direccion).strip()

    return direccion if direccion else None


""" analiza los corredores viales con mayor accidentalidad y genera grafico de barras horizontales """
def analizar(siniestros, carpeta):
    conclusiones = []

    if "DIRECCION" not in siniestros.columns:
        conclusiones.append(
            "No se encontro la columna DIRECCION en el dataset. Analisis de corredores omitido."
        )
        return conclusiones

    siniestros = siniestros.copy()
    siniestros["CORREDOR"] = siniestros["DIRECCION"].apply(_extraer_corredor)

    por_corredor = (
        siniestros["CORREDOR"]
        .dropna()
        .value_counts()
    )

    """ filtra corredores con nombre muy corto o ruido de datos """
    por_corredor = por_corredor[por_corredor.index.str.len() > 2]

    top = por_corredor.index[0]
    total_siniestros = len(siniestros)
    porc_top = (por_corredor.iloc[0] / total_siniestros) * 100

    conclusiones.append(
        f"El corredor con mayor accidentalidad es '{top}', con {por_corredor.iloc[0]:,} siniestros."
    )

    segundo = por_corredor.index[1]
    porc_segundo = (por_corredor.iloc[1] / total_siniestros) * 100
    conclusiones.append(
        f"El segundo corredor mas accidentado es '{segundo}', con {por_corredor.iloc[1]:,} siniestros."
    )

    _graficar(por_corredor.head(15), top, total_siniestros, carpeta)

    return conclusiones


""" genera el grafico de barras horizontales para los corredores viales """
def _graficar(top15, corredor_top, total_siniestros, carpeta):
    fig, ax = plt.subplots(figsize=(12, 8))

    colores = [COLOR_ROJO if c == corredor_top else COLOR_AZUL for c in top15.index]
    barras = ax.barh(top15.index, top15.values, color=colores, height=0.65)
    ax.invert_yaxis()

    """ margen derecho amplio para evitar corte de etiquetas """
    ax.set_xlim(0, top15.max() * 1.25)

    """ etiquetas con conteo y porcentaje sobre el total """
    for barra in barras:
        ancho = barra.get_width()
        porc = (ancho / total_siniestros) * 100
        ax.annotate(
            f" {int(ancho):,} ({porc:.1f}%)",
            xy=(ancho, barra.get_y() + barra.get_height() / 2),
            va="center",
            ha="left",
            fontsize=9,
            fontweight="bold",
            color="#24292F"
        )


    estilizar_grafico(
        ax,
        titulo="Top 15 Corredores Viales con Mayor Accidentalidad",
        xlabel="Número total de siniestros"
    )

    guardar("corredores_viales.png", carpeta)
