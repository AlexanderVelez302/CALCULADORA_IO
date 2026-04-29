import math
import re

def resolver_eoq(texto):
    try:
        # Convertir a minúsculas para búsqueda
        texto_lower = texto.lower()

        # -------------------------------------------------
        # Punto de reorden (ROP)
        # -------------------------------------------------
        demanda_diaria_match = re.search(
            r'(?:demanda\s*diaria|d\s*diaria|d\s*/\s*día|d\s*por\s*día)\s*[\(\)=:]*\s*([\d,]+(?:\.\d+)?)',
            texto_lower
        )
        lead_time_match = re.search(
            r'(?:lead\s*time|tiempo\s*de\s*entrega|tiempo\s*entrega)\s*[\(\)=:]*\s*([\d,]+(?:\.\d+)?)',
            texto_lower
        )

        if demanda_diaria_match and lead_time_match and not re.search(r'(?:costo\s*(?:de|por)?\s*(?:pedido|orden)|costo\s*de\s*mantenimiento|h\s*[=:])', texto_lower):
            demanda_diaria = float(demanda_diaria_match.group(1).replace(',', ''))
            lead_time = float(lead_time_match.group(1).replace(',', ''))

            if demanda_diaria <= 0 or lead_time <= 0:
                return "⚠️ Los parámetros deben ser positivos"

            rop = demanda_diaria * lead_time

            return f"""📍 PUNTO DE REORDEN (ROP)

Parámetros:
- Demanda diaria: {demanda_diaria:.2f} unidades/día
- Tiempo de entrega (Lead Time): {lead_time:.2f} días

Resultado:
- ROP = d × L = {demanda_diaria:.2f} × {lead_time:.2f} = {rop:.0f} unidades
"""
        
        # Buscar patrones más flexibles
        # "Demanda (D) = 10,000" o "D = 10,000" o "d=10000"
        D_match = re.search(r'(?:demanda|d)\s*[\(\)=:]*\s*(?:\()?(?:d)?(?:\))?\s*[=:]\s*([\d,]+)', texto_lower)
        S_match = re.search(r'(?:costo (?:de |por )?(?:pedido|orden)|s)\s*[\(\)=:]*\s*(?:\()?(?:s)?(?:\))?\s*[=:]\s*([\d,]+)', texto_lower)
        H_match = re.search(r'(?:costo de mantenimiento|h)\s*[\(\)=:]*\s*(?:\()?(?:h)?(?:\))?\s*[=:]\s*([\d,\.]+)', texto_lower)
        
        if not (D_match and S_match and H_match):
            return "⚠️ No se encontraron los parámetros D (Demanda), S (Costo de Pedido) y H (Costo de Mantenimiento). Si quieres calcular ROP, escribe Demanda diaria y Tiempo de entrega."
        
        # Limpiar valores (remover comas)
        D = float(D_match.group(1).replace(',', ''))
        S = float(S_match.group(1).replace(',', ''))
        H = float(H_match.group(1).replace(',', ''))
        
        if D <= 0 or S <= 0 or H <= 0:
            return "⚠️ Los parámetros deben ser positivos"
        
        # Calcular EOQ: Q* = sqrt(2DS/H)
        Q_opt = math.sqrt((2 * D * S) / H)
        
        # Calcular costo total
        costo_pedido = (D / Q_opt) * S
        costo_mantenimiento = (Q_opt / 2) * H
        costo_total = costo_pedido + costo_mantenimiento
        
        # Calcular número de pedidos al año
        num_pedidos = D / Q_opt
        
        # Calcular tiempo entre pedidos (en días, asumiendo 365 días/año)
        dias_entre_pedidos = 365 / num_pedidos
        
        resultado = f"""📦 CANTIDAD ECONÓMICA DE PEDIDO (EOQ)

Parámetros:
- Demanda anual (D): {int(D):,} unidades
- Costo de pedido (S): ${S:.2f} por orden
- Costo de mantenimiento (H): ${H:.2f} por unidad/año

Resultados:
- EOQ (Q*): {Q_opt:.0f} unidades por pedido
- Número de pedidos/año: {num_pedidos:.2f}
- Días entre pedidos: {dias_entre_pedidos:.1f} días
- Costo anual de pedidos: ${costo_pedido:.2f}
- Costo anual de mantenimiento: ${costo_mantenimiento:.2f}
- Costo total anual: ${costo_total:.2f}
"""
        
        return resultado
    
    except Exception as e:
        return f"⚠️ Error en cálculo EOQ: {str(e)}"