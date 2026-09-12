import os
import sys
import warnings

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import matplotlib

matplotlib.use("Agg")
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)

from src.config import CARPETA_SALIDA
import src.datos as datos
import src.resumen as resumen
import src.graficos as graficos

import src.analysis.analisis_temporal as analisis_temporal
import src.analysis.analisis_localidades as analisis_localidades
import src.analysis.analisis_causas as analisis_causas
import src.analysis.analisis_vehiculos as analisis_vehiculos
import src.analysis.analisis_actores as analisis_actores
import src.analysis.analisis_sexo as analisis_sexo
import src.analysis.analisis_mapa_calor as analisis_mapa_calor
import src.analysis.analisis_servicio as analisis_servicio

def generar_reporte(ruta_archivo):

    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    try:
        siniestros, actores, vehiculos, hipotesis, diccionario = (
            datos.cargar_datos(ruta_archivo)
        )

    except datos.ErrorDatosEntrada as e:
        print(f"\nError: {e}\n")
        sys.exit(1)

    siniestros, vehiculos, hipotesis = datos.decodificar(
        siniestros,
        vehiculos,
        hipotesis,
        diccionario
    )

    # mostrar resumen general
    resumen.imprimir(
        siniestros,
        actores,
        vehiculos
    )

    # obtener metricas para las tarjetas
    metricas = resumen.obtener_metricas(
        siniestros,
        actores,
        vehiculos
    )

    # generar tarjetas de indicadores
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

    conclusiones += analisis_sexo.analizar(
        actores,
        CARPETA_SALIDA
    )

    conclusiones += analisis_mapa_calor.analizar(
        siniestros,
        CARPETA_SALIDA
    )

    conclusiones += analisis_servicio.analizar(
        vehiculos,
        CARPETA_SALIDA
    )

    _guardar_conclusiones(conclusiones)


    print(
        f"\nreporte y gráficos guardados en la carpeta: "
        f"'{CARPETA_SALIDA}/'"
    )


def _guardar_conclusiones(conclusiones):
    """ guarda conclusiones exclusivamente en archivo de texto sin salida a consola """
    ruta_txt = os.path.join(CARPETA_SALIDA, "conclusiones.txt")

    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write("CONCLUSIONES DEL REPORTE\n\n")
        for i, c in enumerate(conclusiones, 1):
            f.write(f"{i}. {c}\n")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python src/main.py <data/parquet | archivo.xlsx>")
        sys.exit(1)

    generar_reporte(sys.argv[1])
