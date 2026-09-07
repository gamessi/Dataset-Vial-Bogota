#  Dataset Vial Bogotá

> **Dashboard de análisis de siniestralidad vial en Bogotá entre (2015-2020), desarrollado con Python.**

Este proyecto procesa y analiza un conjunto de datos de siniestros viales de Bogotá para identificar patrones relacionados con el **tiempo, localidades, causas, vehículos y personas involucradas**.

El programa genera automáticamente gráficos estadísticos y conclusiones en lenguaje natural, permitiendo obtener una visión general de los principales comportamientos de los datos.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge\&logo=pandas\&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-4C72B0?style=for-the-badge)

---

## Dashboard

Genera un resumen visual con los principales indicadores del conjunto de datos:

![Dashboard](reporte_siniestros/tarjetas_metricas.png)

---

## Lenguaje y librerias utilizadas

| Tecnología         | Uso                               |
| -------------------| --------------------------------- |
|  **Python**        | Lenguaje principal                |
|  **Pandas**        | Procesamiento y análisis de datos |
|  **Matplotlib**    | Generación de gráficos            |
|  **Seaborn**       | Visualización estadística         |
|  **Excel (.xlsx)** | Fuente de datos                   |

---

## Estructura del proyecto

```text
Dataset-Vial-Bogota/
│
├── data/
│   └── siniestros_viales_consolidados_bogota_dc.xlsx
│
├── src/
│   ├── main.py
│   ├── config.py
│   ├── datos.py
│   ├── graficos.py
│   ├── resumen.py
│   │
│   └── analysis/
│       ├── analisis_temporal.py
│       ├── analisis_localidades.py
│       ├── analisis_causas.py
│       ├── analisis_vehiculos.py
│       └── analisis_actores.py
│
├── reporte_siniestros/
│   ├── tarjetas_metricas.png
│   ├── tendencia_anual.png
│   ├── patron_horario.png
│   ├── patron_dia_semana.png
│   ├── top_localidades.png
│   ├── top_causas.png
│   ├── top_vehiculos.png
│   ├── actores_afectados.png
│   ├── distribucion_edad.png
│   └── conclusiones.txt
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Instalación

Clona el repositorio y entra en la carpeta del proyecto.
Después instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## Uso

```bash
py -m src.main data/siniestros_viales_consolidados_bogota_dc.xlsx
```

---

## Resultados

Al finalizar la ejecución se genera automáticamente la carpeta:

```text
reporte_siniestros/
```

Dentro se encuentran los siguientes resultados:

| Archivo                 | Análisis                                        |
| ----------------------- | ----------------------------------------------- |
| `tarjetas_metricas.png` | Indicadores generales                           |
| `tendencia_anual.png`   | Evolución de los siniestros por año             |
| `patron_horario.png`    | Distribución por hora                           |
| `patron_dia_semana.png` | Distribución por día                            |
| `top_localidades.png`   | Localidades con más siniestros                  |
| `top_causas.png`        | Causas más frecuentes                           |
| `top_vehiculos.png`     | Vehículos más involucrados                      |
| `actores_afectados.png` | Personas afectadas según su condición           |
| `distribucion_edad.png` | Distribución de edades                          |
| `conclusiones.txt`      | Principales hallazgos obtenidos automáticamente |


## Fuente de datos

Los datos utilizados corresponden al histórico de siniestros viales de Bogotá D.C. y se encuentran disponibles públicamente en:

**Datos Abiertos Bogotá**

https://datosabiertos.bogota.gov.co/

## Autor

**Camilo Gámez**
    *Estudiante de Ingeniería de Sistemas.*

⭐ Si este proyecto te resulta interesante, puedes darle una estrella al repositorio.
