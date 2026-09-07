"""
USO: python3 main.py siniestros_viales_consolidados_bogota_dc.xlsx
     py main.py siniestros_viales_consolidados_bogota_dc.xlsx

Requisitos: pip install -r requirements.txt
"""

import sys
import os
import warnings

import pandas as pd

warnings.filterwarnings(
    "ignore",
    category=pd.errors.SettingWithCopyWarning
)

import matplotlib

matplotlib.use("Agg")

from src.config import CARPETA_SALIDA
import src.datos as datos
import src.resumen as resumen
import src.graficos as graficos

import src.analysis.analisis_temporal as analisis_temporal
import src.analysis.analisis_localidades as analisis_localidades
import src.analysis.analisis_causas as analisis_causas
import src.analysis.analisis_vehiculos as analisis_vehiculos
import src.analysis.analisis_actores as analisis_actores


def generar_reporte(ruta_archivo):

    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    print("Cargando datos")

    try:
        siniestros, actores, vehiculos, hipotesis, diccionario = (
            datos.cargar_datos(ruta_archivo)
        )

    except datos.ErrorDatosEntrada as e:
        print(f"\nError: {e}\n")
        sys.exit(1)

    print("Decodificando campos en base al diccionario de datos")

    siniestros, vehiculos, hipotesis = datos.decodificar(
        siniestros,
        vehiculos,
        hipotesis,
        diccionario
    )

    # Mostrar resumen general
    resumen.imprimir(
        siniestros,
        actores,
        vehiculos
    )

    # Obtener métricas para las tarjetas
    metricas = resumen.obtener_metricas(
        siniestros,
        actores,
        vehiculos
    )

    # Generar tarjetas de indicadores
    graficos.generar_tarjetas(
        metricas,
        CARPETA_SALIDA
    )

    conclusiones = []

    conclusiones += analisis_temporal.analizar(
        siniestros,
        CARPETA_SALIDA
    )

    conclusiones += analisis_localidades.analizar(
        siniestros,
        CARPETA_SALIDA
    )

    conclusiones += analisis_causas.analizar(
        hipotesis,
        CARPETA_SALIDA
    )

    conclusiones += analisis_vehiculos.analizar(
        vehiculos,
        CARPETA_SALIDA
    )

    conclusiones += analisis_actores.analizar(
        actores,
        CARPETA_SALIDA
    )

    _imprimir_y_guardar_conclusiones(conclusiones)

    print(
        f"\nreporte y gráficos guardados en la carpeta: "
        f"'{CARPETA_SALIDA}/'"
    )


def _imprimir_y_guardar_conclusiones(conclusiones):

    print("CONCLUSIONES AUTOMATICAS")

    for i, c in enumerate(conclusiones, 1):
        print(f"{i}. {c}")

    ruta_txt = os.path.join(
        CARPETA_SALIDA,
        "conclusiones.txt"
    )

    with open(ruta_txt, "w", encoding="utf-8") as f:

        f.write(
            "CONCLUSIONES - SINIESTROS VIALES BOGOTA D.C.\n"
        )

        f.write("=" * 50 + "\n\n")

        for i, c in enumerate(conclusiones, 1):
            f.write(f"{i}. {c}\n")


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "Uso: python3 main.py "
            "siniestros_viales_consolidados_bogota_dc.xlsx"
        )

        sys.exit(1)

    generar_reporte(sys.argv[1])