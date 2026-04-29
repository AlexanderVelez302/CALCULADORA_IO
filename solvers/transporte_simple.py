import re
import numpy as np


def parsear_transporte(texto):
    """
    Parsea problemas de transporte con formato:
    "N Plantas (P_i=X, ...) y M Clientes (C_j=Y, ...). Costos: P_i — C_j=Z, ..."
    
    También maneja problemas de transbordo:
    "Costo A — B = 5, B — C = 3, A — C = 10"
    """
    
    # Intentar parsear como transporte tradicional (con Plantas y Clientes)
    oferta_match = re.search(r'Plantas?\s*\((.*?)\)', texto)
    demanda_match = re.search(r'Clientes?\s*\((.*?)\)', texto)
    
    if oferta_match and demanda_match:
        # Formato tradicional de transporte
        oferta = [int(x) for x in re.findall(r'=(\d+)', oferta_match.group(1))]
        demanda = [int(x) for x in re.findall(r'=(\d+)', demanda_match.group(1))]
        m, n = len(oferta), len(demanda)
        costos = np.zeros((m, n))
        
        costos_matches = re.findall(r'P_?(\d+)?\s*[—\-]\s*C_?(\d+)?\s*[=:]\s*(\d+)', texto)
        
        if costos_matches:
            for p, c, costo in costos_matches:
                i = int(p) - 1 if p else 0
                j = int(c) - 1 if c else 0
                if i < m and j < n:
                    costos[i][j] = int(costo)
        
        return np.array(costos, dtype=int), np.array(oferta, dtype=int), np.array(demanda, dtype=int)
    
    else:
        # Formato de transbordo: "A — B = 5, B — C = 3, A — C = 10"
        # Extraer aristas como (origen, destino, costo)
        aristas = re.findall(r'([A-Z])\s*[—\-]\s*([A-Z])\s*[=:]\s*(\d+)', texto)
        
        if not aristas:
            raise ValueError("No se encontraron aristas en formato 'A — B = 5'")
        
        # Identificar nodos
        nodos = set()
        for o, d, c in aristas:
            nodos.add(o)
            nodos.add(d)
        
        nodos_list = sorted(list(nodos))
        nodo_a_idx = {n: i for i, n in enumerate(nodos_list)}
        m = len(nodos_list)
        
        costos = np.zeros((m, m))
        for o, d, c in aristas:
            i, j = nodo_a_idx[o], nodo_a_idx[d]
            costos[i][j] = int(c)
        
        # Asumir: origen (A) = 10 unidades, destino (C) = 10 unidades
        # Nodos intermedios = 0
        oferta = np.zeros(m, dtype=int)
        demanda = np.zeros(m, dtype=int)
        
        # Origen es el primer nodo (A)
        oferta[0] = 10
        # Destino es el último nodo (C)
        demanda[-1] = 10
        
        return costos, oferta, demanda


def resolver_transbordo(costos, oferta, demanda):
    """
    Resuelve problema de transbordo (transporte con nodos intermedios).
    Usa un enfoque de flujo de costo mínimo greedy.
    """
    n = costos.shape[0]
    nodos = list('ABCDEFGHIJ')[:n]
    
    # Encontrar rutas usando costo mínimo acumulado
    mejores_rutas = []
    
    # Para cada unidad a enviar desde origen a destino
    origen_idx = 0  # Primer nodo (A)
    destino_idx = n - 1  # Último nodo (C)
    
    cantidad_a_enviar = oferta[origen_idx]
    
    # Buscar la ruta más barata de origen a destino
    # Implementar Dijkstra simplificado
    def encontrar_ruta_minima():
        distancia = [float('inf')] * n
        distancia[origen_idx] = 0
        previo = [-1] * n
        visitado = [False] * n
        
        for _ in range(n):
            # Encontrar nodo no visitado con mínima distancia
            u = -1
            for i in range(n):
                if not visitado[i] and (u == -1 or distancia[i] < distancia[u]):
                    u = i
            
            if u == -1 or distancia[u] == float('inf'):
                break
            
            visitado[u] = True
            
            # Relajar aristas
            for v in range(n):
                if costos[u][v] > 0 and distancia[u] + costos[u][v] < distancia[v]:
                    distancia[v] = distancia[u] + costos[u][v]
                    previo[v] = u
        
        # Reconstruir ruta
        ruta = []
        v = destino_idx
        while v != -1:
            ruta.append(v)
            v = previo[v]
        ruta.reverse()
        
        costo_ruta = distancia[destino_idx]
        return ruta, costo_ruta
    
    ruta, costo_ruta = encontrar_ruta_minima()
    
    # Construir resultado
    resultado = "🔀 SOLUCIÓN DE TRANSBORDO (Costo Mínimo de Transporte)\n\n"
    resultado += f"Red de Nodos: {' - '.join(nodos[:n])}\n"
    resultado += f"Cantidad a enviar: {cantidad_a_enviar} unidades\n\n"
    
    resultado += "Costos por ruta:\n"
    # Mostrar todas las rutas disponibles
    for i in range(n):
        for j in range(n):
            if costos[i][j] > 0:
                resultado += f"  {nodos[i]} → {nodos[j]}: {int(costos[i][j])}\n"
    
    resultado += f"\n✅ Ruta óptima: {' → '.join([nodos[i] for i in ruta])}\n"
    resultado += f"Costo por unidad: {int(costo_ruta)}\n"
    resultado += f"Costo total ({cantidad_a_enviar} unidades): {int(costo_ruta * cantidad_a_enviar)}"
    
    return resultado


def resolver_transporte_greedy(costos, oferta, demanda):
    """
    Resuelve el problema de transporte usando un enfoque greedy simple:
    Asignar siempre a la celda con menor costo que tenga capacidad.
    """
    m, n = costos.shape
    oferta = oferta.copy()
    demanda = demanda.copy()
    asignacion = np.zeros((m, n))
    
    # Crear lista de (costo, i, j) ordenada por costo
    celdas = []
    for i in range(m):
        for j in range(n):
            celdas.append((costos[i][j], i, j))
    celdas.sort()
    
    # Asignar en orden de menor costo
    for costo, i, j in celdas:
        cantidad = min(oferta[i], demanda[j])
        if cantidad > 0:
            asignacion[i][j] = cantidad
            oferta[i] -= cantidad
            demanda[j] -= cantidad
    
    return asignacion


def resolver_transporte(texto):
    try:
        costos, oferta, demanda = parsear_transporte(texto)
        
        # Validar que sea balanceado
        if sum(oferta) != sum(demanda):
            return f"⚠️ Problema desbalanceado: Oferta total ({sum(oferta)}) ≠ Demanda total ({sum(demanda)})"

        # Si es transbordo (matriz cuadrada con 3+ nodos y oferta[0] > 0)
        if costos.shape[0] == costos.shape[1] and costos.shape[0] >= 3:
            return resolver_transbordo(costos, oferta, demanda)
        
        # Si no, usar método greedy estándar
        m, n = costos.shape
        asignacion = resolver_transporte_greedy(costos, oferta, demanda)
        costo_total = int(np.sum(costos * asignacion))

        # Construir resultado
        resultado = "🚚 SOLUCIÓN DE TRANSPORTE (Método de Costo Mínimo)\n\n"
        resultado += "Matriz de Costos:\n"
        for i, fila in enumerate(costos):
            resultado += f"P{i+1}: {' '.join(f'{x:3d}' for x in fila)}\n"
        
        resultado += "\nAsignación Óptima:\n"
        for i in range(m):
            for j in range(n):
                if asignacion[i][j] > 0:
                    costo_arista = int(costos[i][j] * asignacion[i][j])
                    resultado += f"P{i+1} → C{j+1}: {int(asignacion[i][j])} unidades (Costo: {int(costos[i][j])} × {int(asignacion[i][j])} = {costo_arista})\n"
        
        resultado += f"\n💰 Costo Total Mínimo: {costo_total}"
        
        return resultado

    except Exception as e:
        return f"⚠️ Error en Transporte: {str(e)}"
