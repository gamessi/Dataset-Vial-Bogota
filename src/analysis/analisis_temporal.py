""" analisis temporal: evolucion anual, hora y dia de la semana """

import matplotlib.pyplot as plt
from src.graficos import (
    guardar,
    estilizar_grafico,
    agregar_etiquetas_barras,
    COLOR_AZUL,
    COLOR_ROJO,
    COLOR_VERDE,
    COLOR_NEUTRO
)

DIAS_ES = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}
ORDEN_DIAS = list(DIAS_ES.keys())


def analizar(siniestros, carpeta):
    """ genera conclusiones y graficos de patrones temporales """
    conclusiones = []
    conclusiones.append(_evolucion_anual(siniestros, carpeta))
    conclusiones.append(_patron_horario(siniestros, carpeta))
    conclusiones.append(_patron_dia_semana(siniestros, carpeta))
    return conclusiones


def _evolucion_anual(siniestros, carpeta):
    """ analiza y grafica la serie temporal de siniestros por anio """
    por_anio = siniestros.groupby("ANIO").size()
    fatales = siniestros[siniestros["GRAVEDAD_DESC"] == "Con Muertos"].groupby("ANIO").size()

    cambio_total = (por_anio.iloc[-1] - por_anio.iloc[0]) / por_anio.iloc[0] * 100
    tendencia = "aumentó" if cambio_total > 0 else "disminuyó"

    nota_covid = ""
    if 2019 in por_anio.index and 2015 in por_anio.index:
        cambio_pre_covid = (por_anio.loc[2019] - por_anio.loc[2015]) / por_anio.loc[2015] * 100
        nota_covid = (
            f" Sin embargo, entre 2015 y 2019 el número se mantuvo relativamente estable "
            f"({cambio_pre_covid:+.1f}%); la caída fuerte ocurre en 2020, coincidiendo con los "
            f"confinamientos por COVID-19, por lo que no debe leerse como una tendencia sostenida de mejora."
        )

    fig, ax = plt.subplots(figsize=(10.5, 5.8))

    """ trazado de lineas con marcadores """
    ax.plot(por_anio.index, por_anio.values, marker="o", linewidth=2.5, markersize=7, color=COLOR_AZUL, label="Total de accidentes")
    ax.plot(fatales.index, fatales.values, marker="s", linewidth=2.2, markersize=6, color=COLOR_ROJO, label="Accidentes con fallecidos")

    """ margen superior generoso para anotaciones sobre puntos """
    ax.set_ylim(0, por_anio.max() * 1.18)

    """ anotacion de puntos en serie total """
    for x, y in zip(por_anio.index, por_anio.values):
        ax.annotate(
            f"{y:,}",
            xy=(x, y),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            fontweight="bold",
            color=COLOR_AZUL
        )

    """ anotacion de puntos en serie fatal """
    for x, y in zip(fatales.index, fatales.values):
        ax.annotate(
            f"{y:,}",
            xy=(x, y),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            fontsize=8.5,
            fontweight="bold",
            color=COLOR_ROJO
        )

    subtitulo = f"Variación total de {cambio_total:+.1f}% entre {por_anio.index.min()} y {por_anio.index.max()} (caída atípica en 2020 por cuarentenas)"
    estilizar_grafico(ax, "Evolución Anual de Siniestros Viales en Bogotá", subtitulo=subtitulo, xlabel="Año", ylabel="Número de accidentes")
    ax.legend(frameon=True, facecolor="white", edgecolor="#D0D7DE", loc="upper right")

    guardar("tendencia_anual.png", carpeta)

    return (
        f"Los accidentes registrados por año {tendencia} un {abs(cambio_total):.1f}% entre "
        f"{por_anio.index.min()} ({por_anio.iloc[0]:,}) y {por_anio.index.max()} ({por_anio.iloc[-1]:,})."
        + nota_covid
    )


def _patron_horario(siniestros, carpeta):
    """ analiza y grafica la distribucion de accidentes por franja horaria """
    por_hora = siniestros["HORA_NUM"].value_counts().sort_index()
    hora_pico = por_hora.idxmax()
    max_casos = por_hora.max()

    fig, ax = plt.subplots(figsize=(12, 6.0))

    """ margen vertical para que la flecha y texto no choquen con titulo """
    ax.set_ylim(0, max_casos * 1.22)

    """ colores destacados para la hora pico y franjas criticas """
    colores = [COLOR_ROJO if h == hora_pico else (COLOR_AZUL if v > por_hora.mean() else COLOR_NEUTRO) for h, v in por_hora.items()]
    barras = ax.bar(por_hora.index, por_hora.values, color=colores, width=0.75, edgecolor="none")

    """ anotacion directa en la hora con mayor pico """
    ax.annotate(
        f"Hora pico: {hora_pico}:00\n({max_casos:,} casos)",
        xy=(hora_pico, max_casos),
        xytext=(0, 16),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        fontweight="bold",
        color=COLOR_ROJO,
        arrowprops=dict(arrowstyle="->", color=COLOR_ROJO, lw=1.2)
    )

    ax.set_xticks(por_hora.index)
    ax.set_xticklabels([f"{h:02d}h" for h in por_hora.index], fontsize=8.5)

    subtitulo = f"Pico crítico a las {hora_pico}:00 hrs con {max_casos:,} siniestros acumulados"
    estilizar_grafico(ax, "Distribución de Accidentes por Hora del Día", subtitulo=subtitulo, xlabel="Hora del día (formato 24h)", ylabel="Número de accidentes")

    guardar("patron_horario.png", carpeta)

    return (
        f"La hora con más accidentes es a las {hora_pico}:00, concentrando {por_hora.max():,} "
        f"registros históricos. Esto suele coincidir con horas pico de tráfico en la ciudad de Bogotá."
    )


def _patron_dia_semana(siniestros, carpeta):
    """ analiza y grafica el volumen de accidentes por dia de la semana """
    por_dia = siniestros["DIA_SEMANA"].value_counts().reindex(ORDEN_DIAS)
    nombres_es = [DIAS_ES[d] for d in por_dia.index]
    dia_pico = DIAS_ES[por_dia.idxmax()]
    total = por_dia.sum()

    fig, ax = plt.subplots(figsize=(10.5, 6.0))

    """ margen vertical para que las etiquetas sobre barras no choquen """
    ax.set_ylim(0, por_dia.max() * 1.18)

    """ resalta el dia con mayor siniestralidad """
    colores = [COLOR_ROJO if d == DIAS_ES[por_dia.idxmax()] else COLOR_VERDE for d in nombres_es]
    ax.bar(nombres_es, por_dia.values, color=colores, width=0.62)

    """ agregar valores exactos y porcentaje del total """
    for contenedor in ax.containers:
        for barra in contenedor:
            alto = barra.get_height()
            porc = (alto / total) * 100
            ax.annotate(
                f"{int(alto):,}\n({porc:.1f}%)",
                xy=(barra.get_x() + barra.get_width() / 2, alto),
                xytext=(0, 6),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
                color="#24292F"
            )

    subtitulo = f"El día con mayor concentración es el {dia_pico} ({por_dia.max():,} accidentes, {por_dia.max()/total*100:.1f}%)"
    estilizar_grafico(ax, "Concentración de Accidentes por Día de la Semana", subtitulo=subtitulo, xlabel="Día de la semana", ylabel="Número de accidentes")

    guardar("patron_dia_semana.png", carpeta)

    return f"El día de la semana con más accidentes es el {dia_pico}, con {por_dia.max():,} registros."


