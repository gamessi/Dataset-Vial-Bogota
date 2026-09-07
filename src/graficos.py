"""Utilidades compartidas para generar y guardar gráficos con estilo consistente."""

import os
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def guardar(nombre_archivo, carpeta):
    """Ajusta el layout y guarda la figura actual de matplotlib; luego la cierra."""
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta, nombre_archivo), dpi=150)
    plt.close()
