import re

def extraer_pert(texto):
    actividades = {}

    lineas = texto.split("\n")

    for l in lineas:
        l = l.strip()

        # buscar patrón tipo A:
        match = re.match(r"([A-Z])\s*:\s*(.+)", l)

        if not match:
            continue

        nombre = match.group(1)
        resto = match.group(2)

        # duración
        duracion_match = re.search(r"(\d+)\s*d", resto)
        if not duracion_match:
            continue

        duracion = int(duracion_match.group(1))

        # predecesores
        predecesores = []

        if "A debe" in resto or "B debe" in resto or "C debe" in resto:
            deps = re.findall(r"([A-Z])", resto.split(";")[0])
            predecesores = deps

        if "y" in resto:
            deps = re.findall(r"([A-Z])", resto.split(";")[0])
            predecesores = deps

        actividades[nombre] = {
            "duracion": duracion,
            "predecesores": predecesores
        }

    return actividades