from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import re

from ai.embeddings import buscar_contexto_libro

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def detectar_tipo_con_ia(pregunta):
    # Heurística inicial: si dice "transbordo", es transporte
    if 'transbordo' in pregunta.lower():
        return 'transporte'
    # Heurística: EOQ - Inventarios
    pregunta_lower = pregunta.lower()
    if 'demanda' in pregunta_lower and 'costo' in pregunta_lower and ('pedido' in pregunta_lower or 'orden' in pregunta_lower) and ('mantenimiento' in pregunta_lower or 'holding' in pregunta_lower):
        return 'eoq'
    if ('demanda diaria' in pregunta_lower or 'demanda/día' in pregunta_lower or 'demanda por día' in pregunta_lower or 'd diaria' in pregunta_lower) and ('lead time' in pregunta_lower or 'tiempo de entrega' in pregunta_lower):
        return 'eoq'
    # Heurística: transporte en lenguaje natural (planta/cliente + costos)
    if ('planta' in pregunta_lower and 'ofrece' in pregunta_lower and 'cliente' in pregunta_lower and 'demanda' in pregunta_lower):
        if re.search(r'p\s*\d+\s*[-—]\s*c\s*\d+\s*=', pregunta_lower):
            return 'transporte'

    # Heurística: si tiene patrón "A — B = costo" sin mencionar "flujo máximo" o "capacidad residual"
    if ('—' in pregunta or '—' in pregunta) and ' = ' in pregunta and 'flujo máximo' not in pregunta.lower():
        if re.search(r'[A-Z]\s*[—\-]\s*[A-Z]\s*=\s*\d+', pregunta):
            return 'transporte'
    
    # Heurística: si menciona "precio" + "costo" + "beneficio" o "almacén" + "área"
    if ('precio' in pregunta.lower() or 'ingresos' in pregunta.lower()) and 'costo' in pregunta.lower():
        if 'beneficio' in pregunta.lower() or 'maximizar' in pregunta.lower():
            return 'nlp'
    
    if 'almacén' in pregunta_lower:
        if ('área' in pregunta_lower or 'area' in pregunta_lower or 'm²' in pregunta_lower or 'm2' in pregunta_lower or 'm^2' in pregunta_lower or '/m' in pregunta_lower):
            return 'nlp'

    # Heurística: Teoría de colas
    if ('tasa de llegada' in pregunta.lower() or 'lambda' in pregunta.lower() or 'λ' in pregunta.lower()):
        if ('tasa de servicio' in pregunta.lower() or 'mu' in pregunta.lower() or 'μ' in pregunta.lower()):
            return 'colas'

    # Heurística: PERT / Ruta crítica
    # Detecta actividades con duración y dependencias tipo "A debe terminar"
    if re.search(r'actividad\s+[a-z]\s*\(\s*\d+\s*[dh]?', pregunta_lower):
        if 'depende de' in pregunta_lower or 'actividades' in pregunta_lower:
            return 'pert'

    if re.search(r'\b[A-Z]\s*:\s*[^\n\r]+\(\s*\d+\s*d[ií]as?\s*\)', pregunta, re.IGNORECASE):
        if re.search(r'debe\s+terminar|precede|depende\s+de|ruta\s+cr[ií]tica|actividades?', pregunta_lower):
            return 'pert'
    if re.search(r'\bactividades\s*:', pregunta_lower):
        if re.search(r'\b[a-z]\s*\([^\)]*\b\d+\s*h\b', pregunta_lower):
            if 'precede' in pregunta_lower or 'debe terminar' in pregunta_lower or 'predecesor' in pregunta_lower:
                return 'pert'
        if 'precede' in pregunta_lower and re.search(r'\b[a-z]\s*\(', pregunta_lower):
            return 'pert'

    # Heurística: Programación Lineal
    # Si hay función objetivo lineal y restricciones, clasificamos como LP
    if ('max z' in pregunta_lower or 'min z' in pregunta_lower or 'maximizar' in pregunta_lower or 'minimizar' in pregunta_lower):
        if ('<=' in pregunta or '>=' in pregunta or '=' in pregunta) and re.search(r'x_\d+|[a-z]\d*', pregunta_lower):
            return 'lp'
    
    contexto = buscar_contexto_libro(pregunta)

    prompt = f"""
Clasifica el siguiente problema de Investigación de Operaciones.

Opciones:

Diferencias clave:

Responde SOLO una palabra.

Problema:
{pregunta}

{contexto}
"""

    try:
        respuesta = llm.invoke(prompt).content.lower().strip()
        return respuesta
    except:
        return "desconocido"