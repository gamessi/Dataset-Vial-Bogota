""" print resumen general en consola antes de entrar al detalle de cada analisis """


def imprimir(siniestros, actores, vehiculos):
    print("RESUMEN GENERAL:")
    print(f"Total de accidentes registrados: {len(siniestros):,}")
    print(f"Total de personas involucradas: {len(actores):,}")
    print(f"Total de vehículos involucrados: {len(vehiculos):,}")
    print(f"Periodo cubierto: {siniestros['FECHA'].min().date()} a {siniestros['FECHA'].max().date()}")
    print()
    print("Distribución por gravedad:")
    print(siniestros["GRAVEDAD_DESC"].value_counts().to_string(name=False, dtype=False))
    print()
