import matplotlib.pyplot as plt
from src.graficos import guardar, estilizar_grafico, COLOR_ROSA, COLOR_AZUL, COLOR_NEUTRO

""" procesa victimas mortales por sexo y genera grafico """
def analizar(actores, carpeta):
    conclusiones = []

    muertos = actores[actores["ESTADO"] == "MUERTO"]
    conteo_sexo = muertos["SEXO"].value_counts(dropna=False)

    """ separar identificados de casos sin informacion """
    con_sexo = muertos[~muertos["SEXO"].isin(["SIN INFORMACION", "NO REPORTADO", "NULL", ""])]["SEXO"].value_counts()
    total_identificados = con_sexo.sum()
    total_fallecidos = len(muertos)

    masculino = con_sexo.get("MASCULINO", 0)
    femenino = con_sexo.get("FEMENINO", 0)
    sin_info = conteo_sexo.get("SIN INFORMACION", 0)

    porc_masc = (masculino / total_identificados * 100) if total_identificados > 0 else 0
    porc_fem = (femenino / total_identificados * 100) if total_identificados > 0 else 0

    fig, ax = plt.subplots(figsize=(10, 5.8))

    categorias = ["Masculino", "Femenino", "Sin Información"]
    valores = [masculino, femenino, sin_info]
    colores = [COLOR_AZUL, COLOR_ROSA, COLOR_NEUTRO]

    """ margen vertical amplio para etiquetas superiores """
    ax.set_ylim(0, max(valores) * 1.20)

    barras = ax.bar(categorias, valores, color=colores, width=0.55)

    """ anota valores exactos y porcentaje sobre casos identificados """
    for barra, val, cat in zip(barras, valores, categorias):
        alto = barra.get_height()
        if cat == "Sin Información":
            texto = f"{val:,}\n({val/total_fallecidos*100:.1f}% total)"
        else:
            texto = f"{val:,}\n({val/total_identificados*100:.1f}%)"

        ax.annotate(
            texto,
            xy=(barra.get_x() + barra.get_width() / 2, alto),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color="#24292F"
        )

    subtitulo = f"Hombres representan {porc_masc:.1f}% ({masculino:,}) de víctimas mortales"
    estilizar_grafico(ax, "Distribución de Fallecidos por Sexo", subtitulo=subtitulo, xlabel="Género", ylabel="Número de personas fallecidas")
    ax.tick_params(axis="x", rotation=0)

    guardar("distribucion_fallecidos.png", carpeta)

    conclusiones.append(
        f"El {porc_masc:.1f}% de las víctimas mortales con género registrado son hombres ({masculino:,} casos), "
        f"frente al {porc_fem:.1f}% de mujeres ({femenino:,} casos)."
    )

    return conclusiones

