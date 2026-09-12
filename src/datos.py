""" carga y transformacion de datos viales optimizados con parquet """

import os
import pandas as pd


class ErrorDatosEntrada(Exception):
    """ excepcion para errores de lectura o formato de datos """
    pass


def cargar_datos(ruta):
    """ lee las 5 tablas del conjunto de datos en formato parquet o excel """
    if not os.path.exists(ruta):
        raise ErrorDatosEntrada(f"la ruta especificada no existe: '{ruta}'")

    """ deteccion de directorio de parquets """
    if os.path.isdir(ruta):
        archivos = {
            "siniestros": os.path.join(ruta, "siniestros.parquet"),
            "actores": os.path.join(ruta, "actores.parquet"),
            "vehiculos": os.path.join(ruta, "vehiculos.parquet"),
            "hipotesis": os.path.join(ruta, "hipotesis.parquet"),
            "diccionario": os.path.join(ruta, "diccionario.parquet"),
        }
        for nombre, arch in archivos.items():
            if not os.path.exists(arch):
                raise ErrorDatosEntrada(f"falta archivo parquet requerido: '{arch}'")

        return (
            pd.read_parquet(archivos["siniestros"], engine="pyarrow"),
            pd.read_parquet(archivos["actores"], engine="pyarrow"),
            pd.read_parquet(archivos["vehiculos"], engine="pyarrow"),
            pd.read_parquet(archivos["hipotesis"], engine="pyarrow"),
            pd.read_parquet(archivos["diccionario"], engine="pyarrow"),
        )

    """ deteccion de archivo parquet individual o carpeta data/parquet complementaria """
    if ruta.endswith(".parquet"):
        directorio = os.path.dirname(ruta) or "."
        return cargar_datos(directorio)

    """ lectura de archivo excel con motor calamine """
    if ruta.endswith((".xlsx", ".xls")):
        """ verificar si existe cache parquet ya generado """
        directorio_cache = os.path.join(os.path.dirname(ruta) or ".", "parquet")
        if os.path.isdir(directorio_cache) and os.path.exists(os.path.join(directorio_cache, "siniestros.parquet")):
            return cargar_datos(directorio_cache)

        try:
            xls = pd.ExcelFile(ruta, engine="calamine")
            return (
                pd.read_excel(xls, sheet_name="SINIESTROS"),
                pd.read_excel(xls, sheet_name="ACTOR_VIAL"),
                pd.read_excel(xls, sheet_name="VEHICULOS"),
                pd.read_excel(xls, sheet_name="HIPOTESIS"),
                pd.read_excel(xls, sheet_name="DICCIONARIO"),
            )
        except Exception as e:
            raise ErrorDatosEntrada(f"error al procesar excel: {e}")

    raise ErrorDatosEntrada(f"formato de archivo no soportado: '{ruta}'")


def _mapa_codigos(diccionario, hoja, campo):
    """ extrae del diccionario un dict codigo a descripcion para una hoja y campo """
    sub = diccionario[(diccionario["HOJA"] == hoja) & (diccionario["CAMPO"] == campo)]
    m = {}
    for cod, desc in zip(sub["CODIGO"], sub["DESCRIPCION"]):
        m[cod] = desc
        m[str(cod)] = desc
        try:
            m[int(cod)] = desc
        except (ValueError, TypeError):
            pass
        try:
            m[float(cod)] = desc
        except (ValueError, TypeError):
            pass
    return m


def decodificar(siniestros, vehiculos, hipotesis, diccionario):
    """ traduce columnas codificadas a texto legible y anade columnas temporales """
    for campo in ["GRAVEDAD", "CLASE", "CHOQUE", "OBJETO_FIJO", "CODIGO_LOCALIDAD", "DISENO_LUGAR"]:
        siniestros[f"{campo}_DESC"] = siniestros[campo].map(_mapa_codigos(diccionario, "SINIESTROS", campo))

    for campo in ["CLASE", "SERVICIO", "MODALIDAD"]:
        vehiculos[f"{campo}_DESC"] = vehiculos[campo].map(_mapa_codigos(diccionario, "VEHICULOS", campo))

    hipotesis["CAUSA_DESC"] = hipotesis["CODIGO_CAUSA"].map(_mapa_codigos(diccionario, "HIPOTESIS", "CODIGO_CAUSA"))

    siniestros["FECHA"] = pd.to_datetime(siniestros["FECHA"], format="%d/%m/%Y", errors="coerce")
    siniestros["ANIO"] = siniestros["FECHA"].dt.year
    siniestros["MES"] = siniestros["FECHA"].dt.month
    siniestros["DIA_SEMANA"] = siniestros["FECHA"].dt.day_name()
    siniestros["HORA_NUM"] = pd.to_datetime(siniestros["HORA"].astype(str), format="%H:%M:%S", errors="coerce").dt.hour

    return siniestros, vehiculos, hipotesis


