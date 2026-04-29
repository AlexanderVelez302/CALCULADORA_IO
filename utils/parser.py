import re

def extraer_valor(texto, variable):
    try:
        patron = rf"{variable}\s*=\s*(\d+)"
        return float(re.search(patron, texto.lower()).group(1))
    except:
        return None