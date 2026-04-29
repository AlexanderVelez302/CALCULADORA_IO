def detectar_tipo(texto):
    texto = texto.lower()

    # -------------------
    # EOQ (inventarios)
    # -------------------
    if "d=" in texto or "s=" in texto or "h=" in texto:
        return "eoq"

    # -------------------
    # PROGRAMACIÓN LINEAL
    # -------------------
    if "maximizar" in texto or "minimizar" in texto:
        return "lp"

    # -------------------
    # COLAS
    # -------------------
    if "lambda" in texto or "μ" in texto or "mu" in texto:
        return "colas"

    # -------------------
    # PERT / CPM
    # -------------------
    if ":" in texto and "," in texto:
        return "pert"

    # -------------------
    # TRANSPORTE (CLAVE NUEVO)
    # -------------------
    if "oferta" in texto and "demanda" in texto:
        return "transporte"

    # -------------------
    # ASIGNAR
    # -------------------
    if "asignar" in texto or "asignacion" in texto:
        return "asignacion"
    
    # -------------------
    # FLUJOS / REDES
    # -------------------
    if "flujo" in texto or "nodo" in texto:
        return "flujo"

    return "desconocido"