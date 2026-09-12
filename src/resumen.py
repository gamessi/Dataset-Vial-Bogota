""" calculo de indicadores globales y metricas ejecutivas de siniestralidad """


def obtener_metricas(siniestros, actores, vehiculos):
    """ calcula indicadores consolidados para el dashboard de control """
    total_accidentes = len(siniestros)
    total_personas = len(actores)
    total_vehiculos = len(vehiculos)

    """ desglose de gravedad del siniestro """
    solo_danos = len(siniestros[siniestros["GRAVEDAD_DESC"] == "Solo Daños"])
    con_heridos = len(siniestros[siniestros["GRAVEDAD_DESC"] == "Con Heridos"])
    con_muertos = len(siniestros[siniestros["GRAVEDAD_DESC"] == "Con Muertos"])

    """ desglose de estado de personas """
    fallecidos = len(actores[actores["ESTADO"] == "MUERTO"])
    heridos = len(actores[actores["ESTADO"] == "HERIDO"])

    """ desglose de servicios de vehiculos """
    particulares = len(vehiculos[vehiculos["SERVICIO_DESC"] == "Particular"])
    publicos = len(vehiculos[vehiculos["SERVICIO_DESC"] == "Público"])

    metricas = {
        "accidentes": total_accidentes,
        "personas": total_personas,
        "vehiculos": total_vehiculos,
        "solo_danos": solo_danos,
        "con_heridos": con_heridos,
        "con_muertos": con_muertos,
        "fallecidos": fallecidos,
        "heridos": heridos,
        "particulares": particulares,
        "publicos": publicos,
        "tasa_letalidad": (con_muertos / total_accidentes * 100) if total_accidentes > 0 else 0,
    }

    return metricas


def imprimir(siniestros, actores, vehiculos):
    """ imprime el resumen en consola con datos """
    print()
    print("Resumen general:")
    print(f"Total de accidentes registrados: {len(siniestros):,}")
    print(f"Total de personas involucradas:  {len(actores):,}")
    print(f"Total de vehículos involucrados: {len(vehiculos):,}")
    print()

    print("Desglose por tipo de servicio:")
    for servicio, cantidad in vehiculos["SERVICIO_DESC"].value_counts().items():
        print(f"  - {servicio}: {cantidad:,}")
    print()

    print("Desglose por gravedad del siniestro:")
    for gravedad, cantidad in siniestros["GRAVEDAD_DESC"].value_counts().items():
        print(f"  - {gravedad}: {cantidad:,}")
    print()
