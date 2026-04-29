import re

def parsear_lp(texto):
    lineas = texto.strip().split("\n")

    c = []
    A = []
    b = []

    # --- FUNCIÓN OBJETIVO ---
    for linea in lineas:
        if "max" in linea.lower() or "min" in linea.lower():
            numeros = re.findall(r'[-+]?\d+', linea)
            c = [-int(n) for n in numeros]  # negativo porque linprog minimiza

    # --- RESTRICCIONES ---
    for linea in lineas:
        if "<=" in linea:
            partes = linea.split("<=")
            izquierda = partes[0]
            derecha = int(partes[1].strip())

            coef = re.findall(r'[-+]?\d+', izquierda)

            if len(coef) >= 2:
                A.append([int(coef[0]), int(coef[1])])
                b.append(derecha)

    return c, A, b