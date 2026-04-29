import re
import numpy as np
from scipy.optimize import fminbound, minimize


def resolver_nlp(texto):
    """
    Resuelve problemas de optimización no lineal.
    Soporta:
    - Beneficio con función de demanda no lineal: P = a - bQ, C = cQ + d
    - Área de almacén: Minimizar C = ax + by sujeto a xy = K
    """
    try:
        texto_lower = texto.lower()
        
        # Detectar tipo de problema
        if 'precio' in texto_lower and 'costo' in texto_lower and 'beneficio' in texto_lower:
            return resolver_beneficio_no_lineal(texto)
        elif 'almacén' in texto_lower or 'area' in texto_lower or 'xy' in texto_lower:
            return resolver_area_almacen(texto)
        else:
            return "⚠️ Tipo de problema NLP no identificado"
    
    except Exception as e:
        return f"⚠️ Error en NLP: {str(e)}"


def resolver_beneficio_no_lineal(texto):
    """
    Resuelve: Maximizar B = P*Q - C donde P y C son funciones de Q
    Formato: "Precio P = a - bQ. Costo total C = cQ + d. Maximizar beneficio"
    """
    # Extraer función de precio: P = a - bQ
    precio_match = re.search(r'precio\s+p\s*=\s*([\d\.]+)\s*[-\+]\s*([\d\.]+)\s*q', texto.lower())
    if not precio_match:
        return "⚠️ No se encontró función de precio en formato 'P = a - bQ'"
    
    a = float(precio_match.group(1))
    b = float(precio_match.group(2))
    
    # Extraer función de costo: C = cQ + d (manejar comas y puntos)
    costo_match = re.search(r'costo\s+(?:total\s+)?c\s*=\s*([\d\.]+)\s*q\s*[+\-]\s*([\d,\.]+)', texto.lower())
    if not costo_match:
        return "⚠️ No se encontró función de costo en formato 'C = cQ + d'"
    
    c = float(costo_match.group(1))
    d = float(costo_match.group(2).replace(',', ''))  # Remover comas
    
    # Función de beneficio: B = (a - bQ)*Q - (cQ + d) = -bQ² + (a-c)Q - d
    # Derivada: dB/dQ = -2bQ + (a-c)
    # Óptimo: Q* = (a-c)/(2b)
    
    Q_opt = (a - c) / (2 * b)
    P_opt = a - b * Q_opt
    B_opt = P_opt * Q_opt - (c * Q_opt + d)
    
    # Verificar que sea máximo (segunda derivada negativa)
    segunda_derivada = -2 * b
    es_maximo = segunda_derivada < 0
    
    resultado = f"""📈 OPTIMIZACIÓN DE INGRESOS (Programación No Lineal)

Funciones dadas:
- Precio: P = {a} - {b}Q
- Costo total: C = {c}Q + {d}
- Beneficio: B = P*Q - C = -{b}Q² + {a-c}Q - {d}

Solución óptima:
- Cantidad óptima (Q*): {Q_opt:.0f} unidades
- Precio óptimo (P*): ${P_opt:.2f} por unidad
- Beneficio máximo: ${B_opt:.2f}

Análisis matemático:
- Primera derivada: dB/dQ = -{2*b}Q + {a-c}
- Punto crítico: Q* = (a-c)/(2b) = ({a}-{c})/(2×{b}) = {Q_opt:.0f}
- Segunda derivada: d²B/dQ² = {segunda_derivada} {'< 0 → Máximo ✅' if es_maximo else '> 0 → Mínimo'}

Verificación:
- Ingresos totales: {P_opt:.2f} × {Q_opt:.0f} = ${P_opt * Q_opt:.2f}
- Costos totales: {c}×{Q_opt:.0f} + {d} = ${c * Q_opt + d:.2f}
- Beneficio neto: ${P_opt * Q_opt:.2f} - ${c * Q_opt + d:.2f} = ${B_opt:.2f}
"""
    
    return resultado


def resolver_area_almacen(texto):
    """
    Resuelve: Minimizar C = cx + dy sujeto a xy = K
    Formato: "área de K m². Costo pared frontal ax/m. Otras tres paredes b/m."
    """
    # Extraer área (buscar "1000 m²", "1000 m2" o "1000 , m^2")
    area_match = re.search(r'(\d[\d,\.]*)\s*,?\s*m(?:\^?2|²|2)?', texto.lower())
    if not area_match:
        return "⚠️ No se encontró el área del almacén en formato 'X m²'"
    
    K = float(area_match.group(1).replace(',', ''))
    
    # Extraer costos: buscar números seguidos de "/m" o "por m"
    # Buscar "100/m" o "100/metros" etc.
    costos_matches = re.findall(r'(\d+)\s*(?:/|por)\s*m(?:etro)?s?', texto.lower())
    
    if len(costos_matches) < 2:
        return "⚠️ No se encontraron los costos de las paredes en formato 'X/m'"
    
    a = float(costos_matches[0])  # Costo pared frontal
    b = float(costos_matches[1])  # Costo otras paredes
    
    # Función objetivo: C = ax + b(x + 2y) donde y = K/x
    # C(x) = ax + b(x + 2K/x) = (a+b)x + 2bK/x
    
    # Derivada: dC/dx = (a+b) - 2bK/x²
    # Óptimo: x* = sqrt(2bK/(a+b))
    
    x_opt = np.sqrt(2 * b * K / (a + b))
    y_opt = K / x_opt
    C_opt = a * x_opt + b * (x_opt + 2 * y_opt)
    
    resultado = f"""🏭 OPTIMIZACIÓN DE ALMACÉN (Programación No Lineal)

Problema:
- Área del almacén: {int(K)} m²
- Costo pared frontal: ${a}/m
- Costo otras tres paredes: ${b}/m

Restricción: xy = {int(K)}
Objetivo: Minimizar C = {a}x + {b}(x + 2y) = {a+b}x + {2*b}y

Solución óptima:
- Ancho (x): {x_opt:.2f} m
- Largo (y): {y_opt:.2f} m
- Costo total mínimo: ${C_opt:.2f}

Análisis matemático:
- Función de costo: C(x) = {a+b}x + {2*b*K}/x
- Primera derivada: dC/dx = {a+b} - {2*b*K}/x²
- Punto crítico: x* = √({2*b*K}/{a+b}) = √({2*b*K/(a+b):.1f}) = {x_opt:.2f}
- Segunda derivada: d²C/dx² = {4*b*K}/(x³) > 0 → Mínimo ✅

Verificación:
- Área: {x_opt:.2f} × {y_opt:.2f} = {x_opt*y_opt:.1f} m² ✓
- Costo pared frontal: ${a} × {x_opt:.2f} = ${a*x_opt:.2f}
- Costo otras 3 paredes: ${b} × ({x_opt:.2f} + 2×{y_opt:.2f}) = ${b*(x_opt+2*y_opt):.2f}
- Costo total: ${C_opt:.2f}
"""
    
    return resultado
