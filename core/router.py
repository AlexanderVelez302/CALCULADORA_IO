from core.detector_ia import detectar_tipo_con_ia

from solvers.eoq import resolver_eoq
from solvers.colas import resolver_colas
from solvers.pert import resolver_pert
from solvers.flujo import resolver_flujo
from solvers.lp import resolver_lp
from solvers.nlp import resolver_nlp
from solvers.transporte_simple import resolver_transporte
from solvers.asignacion import resolver_asignacion

from ai.groq import explicar_con_ia


def resolver(pregunta):
    tipo = detectar_tipo_con_ia(pregunta)

    # -------------------
    # EOQ
    # -------------------
    if tipo == "eoq":
        resultado = resolver_eoq(pregunta)

    # -------------------
    # COLAS
    # -------------------
    elif tipo == "colas":
        resultado = resolver_colas(pregunta)

    # -------------------
    # PERT
    # -------------------
    elif tipo == "pert":
        resultado = resolver_pert(pregunta)

    # -------------------
    # FLUJO / REDES
    # -------------------
    elif tipo == "flujo":
        resultado = resolver_flujo(pregunta)

    # -------------------
    # PROGRAMACIÓN LINEAL
    # -------------------
    elif tipo == "lp":
        resultado = resolver_lp(pregunta)

    # -------------------
    # PROGRAMACIÓN NO LINEAL
    # -------------------
    elif tipo == "nlp":
        resultado = resolver_nlp(pregunta)

    # -------------------
    # TRANSPORTE
    # -------------------
    elif tipo == "transporte":
        resultado = resolver_transporte(pregunta)

    # -------------------
    # ASIGNACION
    # -------------------
    elif tipo == "asignacion":
        resultado = resolver_asignacion(pregunta)

    # -------------------
    # DESCONOCIDO
    # -------------------
    else:
        resultado = "⚠️ Tipo de problema no identificado"

    if resultado.startswith("⚠️") or resultado.startswith("Error"):
        return f"\n{resultado}\n"

    # IA explicativa (siempre al final)
    explicacion = explicar_con_ia(pregunta, resultado)

    return f"""
{resultado}

-------------------
📖 {explicacion}
"""


def router(pregunta):
    """Compatibilidad retroactiva para tests/código que importan `router`."""
    return resolver(pregunta)