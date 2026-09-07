"""Patrones temporales: evolución anual, hora del día y día de la semana."""

import matplotlib.pyplot as plt
from src.graficos import guardar

DIAS_ES = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
           "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}
ORDEN_DIAS = list(DIAS_ES.keys())


def analizar(siniestros, carpeta):
    conclusiones = []
    conclusiones.append(_evolucion_anual(siniestros, carpeta))
    conclusiones.append(_patron_horario(siniestros, carpeta))
    conclusiones.append(_patron_dia_semana(siniestros, carpeta))
    return conclusiones


def _evolucion_anual(siniestros, carpeta):
    por_anio = siniestros.groupby("ANIO").size()
    fatales = siniestros[siniestros["GRAVEDAD_DESC"] == "Con Muertos"].groupby("ANIO").size()

    cambio_total = (por_anio.iloc[-1] - por_anio.iloc[0]) / por_anio.iloc[0] * 100
    tendencia = "aumentó" if cambio_total > 0 else "disminuyó"

    # 2020 tuvo confinamientos por COVID-19 que distorsionan la lectura de "tendencia":
    # se compara aparte 2015->2019 para no confundir un evento atípico con una mejora sostenida.
    nota_covid = ""
    if 2019 in por_anio.index and 2015 in por_anio.index:
        cambio_pre_covid = (por_anio.loc[2019] - por_anio.loc[2015]) / por_anio.loc[2015] * 100
        nota_covid = (
            f" Sin embargo, entre 2015 y 2019 el número se mantuvo relativamente estable "
            f"({cambio_pre_covid:+.1f}%); la caída fuerte ocurre en 2020, coincidiendo con los "
            f"confinamientos por COVID-19, por lo que no debe leerse como una tendencia sostenida de mejora."
        )

    plt.figure(figsize=(9, 5))
    por_anio.plot(kind="line", marker="o", label="Total accidentes")
    fatales.plot(kind="line", marker="o", label="Con muertos")
    plt.title("Evolución anual de siniestros viales en Bogotá")
    plt.xlabel("Año")
    plt.ylabel("Número de accidentes")
    plt.legend()
    guardar("tendencia_anual.png", carpeta)

    return (
        f"Los accidentes registrados por año {tendencia} un {abs(cambio_total):.1f}% entre "
        f"{por_anio.index.min()} ({por_anio.iloc[0]:,}) y {por_anio.index.max()} ({por_anio.iloc[-1]:,})."
        + nota_covid
    )


def _patron_horario(siniestros, carpeta):
    por_hora = siniestros["HORA_NUM"].value_counts().sort_index()
    hora_pico = por_hora.idxmax()

    plt.figure(figsize=(9, 5))
    por_hora.plot(kind="bar", color="steelblue")
    plt.title("Accidentes por hora del día")
    plt.xlabel("Hora")
    plt.ylabel("Número de accidentes")
    guardar("patron_horario.png", carpeta)

    return (
        f"La hora con más accidentes es a las {hora_pico}:00, concentrando {por_hora.max():,} "
        f"registros históricos. Esto suele coincidir con horas pico de tráfico en la ciudad de Bogotá."
    )


def _patron_dia_semana(siniestros, carpeta):
    por_dia = siniestros["DIA_SEMANA"].value_counts().reindex(ORDEN_DIAS)
    dia_pico = DIAS_ES[por_dia.idxmax()]

    plt.figure(figsize=(9, 5))
    por_dia.rename(index=DIAS_ES).plot(kind="bar", color="indianred")
    plt.title("Accidentes por día de la semana")
    plt.ylabel("Número de accidentes")
    guardar("patron_dia_semana.png", carpeta)

    return f"El día de la semana con más accidentes es el {dia_pico}, con {por_dia.max():,} registros."
