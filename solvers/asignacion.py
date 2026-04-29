import numpy as np
import re
from scipy.optimize import linear_sum_assignment


def parsear_asignacion(texto):
    texto = texto.lower()

    # extraer matriz de costos (números en orden)
    numeros = list(map(int, re.findall(r'-?\d+', texto)))

    if len(numeros) < 4:
        return None

    n = int(len(numeros) ** 0.5)

    if n * n != len(numeros):
        return None

    matriz = np.array(numeros).reshape(n, n)

    return matriz


def resolver_asignacion(texto):
    try:
        costos = parsear_asignacion(texto)

        if costos is None:
            return "⚠️ No se pudo interpretar la matriz de asignación"

        # algoritmo húngaro
        filas, columnas = linear_sum_assignment(costos)

        asignacion = np.zeros_like(costos)

        costo_total = 0

        resultado_lineas = []

        for i, j in zip(filas, columnas):
            asignacion[i][j] = 1
            costo_total += costos[i][j]
            resultado_lineas.append(f"P{i+1} → T{j+1} = {costos[i][j]}")

        return f"""
📌 ASIGNACIÓN ÓPTIMA (Húngaro)

Matriz de costos:
{costos}

Asignaciones:
{chr(10).join(resultado_lineas)}

💰 Costo mínimo total = {costo_total}
"""

    except Exception as e:
        return f"Error en asignación: {e}"