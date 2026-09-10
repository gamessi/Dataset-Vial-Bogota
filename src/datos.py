import pandas as pd

def cargar_datos(ruta):
    """ lee las 5 hojas del archivo y las devuelve como DataFrames separados """
    xls = pd.ExcelFile(ruta, engine="calamine")
    return (
        pd.read_excel(xls, sheet_name="SINIESTROS"),
        pd.read_excel(xls, sheet_name="ACTOR_VIAL"),
        pd.read_excel(xls, sheet_name="VEHICULOS"),
        pd.read_excel(xls, sheet_name="HIPOTESIS"),
        pd.read_excel(xls, sheet_name="DICCIONARIO"),
    )


def _mapa_codigos(diccionario, hoja, campo):
    """ extrae del DICCIONARIO un dict {codigo: descripcion} para una hoja/campo """
    sub = diccionario[(diccionario["HOJA"] == hoja) & (diccionario["CAMPO"] == campo)]
    return dict(zip(sub["CODIGO"], sub["DESCRIPCION"]))


def decodificar(siniestros, vehiculos, hipotesis, diccionario):
    """ traduce columnas codificadas a texto legible y añade columnas de fecha/hora"""
    for campo in ["GRAVEDAD", "CLASE", "CHOQUE", "OBJETO_FIJO", "CODIGO_LOCALIDAD", "DISENO_LUGAR"]:
        siniestros[f"{campo}_DESC"] = siniestros[campo].map(_mapa_codigos(diccionario, "SINIESTROS", campo))

    for campo in ["CLASE", "SERVICIO", "MODALIDAD"]:
        vehiculos[f"{campo}_DESC"] = vehiculos[campo].map(_mapa_codigos(diccionario, "VEHICULOS", campo))

    hipotesis["CAUSA_DESC"] = hipotesis["CODIGO_CAUSA"].map(_mapa_codigos(diccionario, "HIPOTESIS", "CODIGO_CAUSA"))

    siniestros["FECHA"] = pd.to_datetime(siniestros["FECHA"], format="%d/%m/%Y", errors="coerce")
    siniestros["ANIO"] = siniestros["FECHA"].dt.year
    siniestros["MES"] = siniestros["FECHA"].dt.month
    siniestros["DIA_SEMANA"] = siniestros["FECHA"].dt.day_name()
    siniestros["HORA_NUM"] = pd.to_datetime(siniestros["HORA"], format="%H:%M:%S", errors="coerce").dt.hour

    return siniestros, vehiculos, hipotesis
