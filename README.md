# Dataset Vial Bogotá

> **Análisis de siniestralidad vial en Bogotá (2015–2020) desarrollado con Python.**

Procesa un conjunto de datos de siniestros viales para identificar patrones por **tiempo, localidades, causas, vehículos, actores y servicio vehicular**. Genera gráficos estadísticos y conclusiones automáticamente.

---

## Dashboard

![Dashboard](reporte_siniestros/tarjetas_metricas.png)

---

## Instalación

```bash
git clone https://github.com/gamessi/Dataset-Vial-Bogota
pip install -r requirements.txt
```

---

## Uso

Con datos en parquet *(recomendado)*:

```bash
python src/main.py data/parquet
```

Con el archivo Excel original:

```bash
python src/main.py data/siniestros_viales_consolidados_bogota_dc.xlsx
```

> Al usar el archivo Excel por primera vez, el programa genera automáticamente los archivos `.parquet` en `data/parquet/` para acelerar ejecuciones futuras.

---

## Resultados

Los archivos se generan en la carpeta `reporte_siniestros/`:

| Archivo                       | Análisis                                        |
|---|---|
| `tarjetas_metricas.png`       | Dasboard                                        |
| `tendencia_anual.png`         | Evolución de siniestros por año                 |
| `patron_horario.png`          | Distribución por hora del día                   |
| `patron_dia_semana.png`       | Distribución por día de la semana               |
| `top_localidades.png`         | Localidades con más siniestros                  |
| `mapa_calor_localidades.png`  | Mapa de calor de sinestros por localidad        |
| `top_causas.png`              | Causas más frecuentes                           |
| `top_vehiculos.png`           | Vehículos más involucrados                      |
| `actores_afectados.png`       | Personas afectadas por rol                      |
| `distribucion_edad.png`       | Distribución de edades de las víctimas          |
| `distribucion_fallecidos.png` | Fallecidos por genéro                           |
| `analisis_servicio.png`       | Siniestros por tipo de servicio vehicular       |
| `conclusiones.txt`            | Hallazgos principales generados automáticamente |

---

## Estructura del proyecto

```text
Dataset-Vial-Bogota/
│
├── data/
│   ├── siniestros_viales_consolidados_bogota_dc.xlsx
│   ├── poligonos-localidades.geojson
│   └── parquet/
│       └── *.parquet
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
│       ├── analisis_actores.py
│       ├── analisis_mapa_calor.py
│       ├── analisis_servicio.py
│       └── analisis_sexo.py
│
├── reporte_siniestros/
│   ├── conclusiones.txt   
│   └── *.png
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## Tecnologías

| Librería | Uso |
|---|---|
| **Pandas**    | Procesamiento y análisis de datos     |
| **Matplotlib**| Generación de gráficos                |
| **Seaborn**   | Visualización estadística             |
| **GeoPandas** | Mapas de calor                        |
| **PyArrow**   | Lectura/escritura de archivos Parquet |

---

## Fuente de datos

- **Dataset:** [Datos Abiertos Bogotá](https://datosabiertos.bogota.gov.co/)
- **GeoJSON:** [Laboratorio Urbano Bogotá](https://bogota-laburbano.opendatasoft.com/explore/dataset/poligonos-localidades/table/)

---

## Autor

**Camilo Gámez** — **Estudiante de Ingeniería de Sistemas**
