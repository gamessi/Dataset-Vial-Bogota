""" muestra el resumen general y las metricas del proyecto """


def obtener_metricas(siniestros, actores, vehiculos):
    """ calcula las metricas principales del conjunto de datos """

    metricas = {
        "accidentes": len(siniestros),
        "personas": len(actores),
        "vehiculos": len(vehiculos),
        "fecha_inicio": siniestros["FECHA"].min(),
        "fecha_fin": siniestros["FECHA"].max(),
    }

    return metricas


def imprimir(siniestros, actores, vehiculos):
    """ imprime el resumen en consola """

    print()
    print("Resumen general:")

    print(f"Total de accidentes registrados: {len(siniestros):,}")
    print(f"Total de personas involucradas:  {len(actores):,}")
    print(f"Total de vehículos involucrados: {len(vehiculos):,}")

    print(
        f"Periodo cubierto: "
        f"{siniestros['FECHA'].min().date()} a "
        f"{siniestros['FECHA'].max().date()}"
    )

    print()

    print("Distribución por gravedad:")

    print(
        siniestros["GRAVEDAD_DESC"]
        .value_counts()
        .to_string(name=False, dtype=False)
    )

    print()