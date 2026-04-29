import numpy as np
import re


# =========================
# PARSEO FLEXIBLE
# =========================
def parsear_transporte(texto):
    """
    Parsea problemas de transporte con formato:
    "N Plantas (P_i=X, ...) y M Clientes (C_j=Y, ...). Costos: P_i — C_j=Z, ..."
    """
    
    # Extraer oferta (plantas)
    oferta_match = re.search(r'Plantas?\s*\((.*?)\)', texto)
    oferta = []
    if oferta_match:
        plantas_str = oferta_match.group(1)
        oferta = [int(x) for x in re.findall(r'=(\d+)', plantas_str)]
    
    # Extraer demanda (clientes)
    demanda_match = re.search(r'Clientes?\s*\((.*?)\)', texto)
    demanda = []
    if demanda_match:
        clientes_str = demanda_match.group(1)
        demanda = [int(x) for x in re.findall(r'=(\d+)', clientes_str)]
    
    # Extraer matriz de costos
    m, n = len(oferta), len(demanda)
    costos = np.zeros((m, n))
    
    # Buscar pares P_i — C_j=costo
    costos_matches = re.findall(r'P_?(\d+)?\s*[—\-]\s*C_?(\d+)?\s*[=:]\s*(\d+)', texto)
    
    if costos_matches:
        for p, c, costo in costos_matches:
            i = int(p) - 1 if p else 0  # P_1, P_2, ... o posición
            j = int(c) - 1 if c else 0  # C_1, C_2, ... o posición
            if i < m and j < n:
                costos[i][j] = int(costo)
    else:
        # Fallback: extraer todos los números después de "Costos:"
        costos_section = texto.split('Costos:')[-1]
        numeros = [int(x) for x in re.findall(r'\d+', costos_section)]
        costos = np.array(numeros[:m*n]).reshape(m, n)
    
    return np.array(costos, dtype=int), np.array(oferta, dtype=int), np.array(demanda, dtype=int)


# =========================
# VOGEL (INICIAL)
# =========================
def vogel(costos, oferta, demanda):
    m, n = costos.shape
    oferta = oferta.copy()
    demanda = demanda.copy()

    asignacion = np.zeros((m, n))

    while np.any(oferta > 0) and np.any(demanda > 0):

        penal_filas = []
        penal_cols = []

        for i in range(m):
            costos_validos = [costos[i][j] for j in range(n) if demanda[j] > 0]
            if len(costos_validos) >= 2:
                costos_validos.sort()
                penal_filas.append((costos_validos[1] - costos_validos[0], i))

        for j in range(n):
            costos_validos = [costos[i][j] for i in range(m) if oferta[i] > 0]
            if len(costos_validos) >= 2:
                costos_validos.sort()
                penal_cols.append((costos_validos[1] - costos_validos[0], j))

        if penal_filas and (not penal_cols or max(penal_filas)[0] >= max(penal_cols)[0]):
            _, i = max(penal_filas)
            j = min((j for j in range(n) if demanda[j] > 0), key=lambda j: costos[i][j])
        else:
            _, j = max(penal_cols)
            i = min((i for i in range(m) if oferta[i] > 0), key=lambda i: costos[i][j])

        cantidad = min(oferta[i], demanda[j])

        asignacion[i][j] = cantidad
        oferta[i] -= cantidad
        demanda[j] -= cantidad

    return asignacion


# =========================
# COSTO TOTAL
# =========================
def costo_total(costos, asignacion):
    return np.sum(costos * asignacion)


# =========================
# ENCONTRAR u y v
# =========================
def calcular_uv(costos, asignacion):
    m, n = costos.shape

    u = [None] * m
    v = [None] * n

    u[0] = 0

    cambios = True

    while cambios:
        cambios = False
        for i in range(m):
            for j in range(n):
                if asignacion[i][j] > 0:
                    if u[i] is not None and v[j] is None:
                        v[j] = costos[i][j] - u[i]
                        cambios = True
                    elif v[j] is not None and u[i] is None:
                        u[i] = costos[i][j] - v[j]
                        cambios = True

    return u, v


# =========================
# COSTOS REDUCIDOS
# =========================
def encontrar_entrada(costos, asignacion, u, v):
    m, n = costos.shape

    min_val = 0
    pos = None

    for i in range(m):
        for j in range(n):
            if asignacion[i][j] == 0:
                costo_reducido = costos[i][j] - (u[i] + v[j])

                if costo_reducido < min_val:
                    min_val = costo_reducido
                    pos = (i, j)

    return pos, min_val


# =========================
# CONSTRUIR CICLO
# =========================
def construir_ciclo(asignacion, start):
    m, n = asignacion.shape
    i0, j0 = start

    posiciones = [(i0, j0)]

    filas = {}
    cols = {}

    for i in range(m):
        filas[i] = [j for j in range(n) if asignacion[i][j] > 0 or (i, j) == start]

    for j in range(n):
        cols[j] = [i for i in range(m) if asignacion[i][j] > 0 or (i, j) == start]

    def backtrack(path, used_rows, used_cols):
        i, j = path[-1]

        if len(path) > 3 and i == i0 and j == j0:
            return path

        # mover horizontal
        for jj in filas[i]:
            if jj != j and (i, jj) not in path:
                res = backtrack(path + [(i, jj)], used_rows, used_cols)
                if res:
                    return res

        # mover vertical
        for ii in cols[j]:
            if ii != i and (ii, j) not in path:
                res = backtrack(path + [(ii, j)], used_rows, used_cols)
                if res:
                    return res

        return None

    return backtrack([start], set(), set())


# =========================
# AJUSTE DEL CICLO
# =========================
def ajustar(asignacion, ciclo):
    ciclo = ciclo[:-1]  # quitar repetido final

    signos = [1, -1] * (len(ciclo)//2)

    cantidades = [asignacion[i][j] for (i, j) in ciclo if asignacion[i][j] > 0]

    theta = min(cantidades) if cantidades else 0

    for k, (i, j) in enumerate(ciclo):
        if k % 2 == 0:
            asignacion[i][j] += theta
        else:
            asignacion[i][j] -= theta
            if asignacion[i][j] == 0:
                asignacion[i][j] = 0

    return asignacion


# =========================
# SOLVER FINAL (VERSIÓN SIMPLIFICADA - VOGEL SOLAMENTE)
# =========================
def resolver_transporte(texto):
    try:
        costos, oferta, demanda = parsear_transporte(texto)
        m, n = costos.shape
        
        # Validar que sea balanceado
        if sum(oferta) != sum(demanda):
            return f"⚠️ Problema desbalanceado: Oferta total ({sum(oferta)}) ≠ Demanda total ({sum(demanda)})"

        # Usar método de Vogel para obtener solución inicial
        asignacion = vogel(costos, oferta, demanda)
        costo_minimo = costo_total(costos, asignacion)

        # Construir resultado
        resultado = "🚚 SOLUCIÓN DE TRANSPORTE (Método de Vogel)\n\n"
        resultado += "Matriz de Costos:\n"
        for i, fila in enumerate(costos):
            resultado += f"P{i+1}: {' '.join(f'{x:3d}' for x in fila)}\n"
        
        resultado += "\nAsignación Óptima:\n"
        for i in range(m):
            for j in range(n):
                if asignacion[i][j] > 0:
                    costo_arista = int(costos[i][j] * asignacion[i][j])
                    resultado += f"P{i+1} → C{j+1}: {int(asignacion[i][j])} unidades (Costo: {int(costos[i][j])} × {int(asignacion[i][j])} = {costo_arista})\n"
        
        resultado += f"\n💰 Costo Total Mínimo: {int(costo_minimo)}"
        
        return resultado

    except Exception as e:
        return f"⚠️ Error en Transporte: {str(e)}"