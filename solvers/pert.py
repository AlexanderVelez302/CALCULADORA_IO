import re


def resolver_pert(texto):
    try:
        actividades = {}

        # -------------------------
        # 1. LIMPIEZA REAL
        # -------------------------
        texto = texto.replace("●", "\n")
        texto = texto.replace(".", "")
        texto = texto.replace(";", ",")

        lineas = [l.strip() for l in texto.split("\n") if l.strip()]

        # -------------------------
        # 2. PARSEO INTELIGENTE
        # -------------------------
        patrones = []

        for linea in lineas:
            patrones.extend(re.findall(r"([A-Z])\s*:\s*([^\n]+)", linea))
            patrones.extend(re.findall(r"([A-Z])\s*\(([^)]*\d+[^)]*)\)", linea))

        vistos = set()
        for nombre, resto in patrones:
            if nombre in vistos:
                continue
            vistos.add(nombre)

            d_match = re.search(r"(\d+)", resto)
            if not d_match:
                continue

            duracion = int(d_match.group(1))

            bloque = resto[:d_match.start()]
            predecesores = re.findall(r"\b([A-Z])\b", bloque)
            predecesores = [p for p in predecesores if p != nombre]

            actividades[nombre] = {
                "duracion": duracion,
                "predecesores": list(set(predecesores)),
                "ES": 0, "EF": 0,
                "LS": 0, "LF": 0
            }

        if not actividades:
            return "⚠️ No se pudieron extraer actividades"

        # -------------------------
        # 3. ORDEN TOPOLOGICO
        # -------------------------
        orden = []
        visitado = set()

        def dfs(n):
            if n in visitado:
                return
            visitado.add(n)

            for p in actividades[n]["predecesores"]:
                if p in actividades:
                    dfs(p)

            orden.append(n)

        for a in actividades:
            dfs(a)

        # -------------------------
        # 4. FORWARD PASS
        # -------------------------
        for act in orden:
            data = actividades[act]
            preds = data["predecesores"]

            if preds:
                ES = max(actividades[p]["EF"] for p in preds)
            else:
                ES = 0

            EF = ES + data["duracion"]

            data["ES"] = ES
            data["EF"] = EF

        # -------------------------
        # 5. TIEMPO TOTAL
        # -------------------------
        max_tiempo = max(a["EF"] for a in actividades.values())

        # -------------------------
        # 6. BACKWARD PASS (CORREGIDO)
        # -------------------------
        for act in actividades:
            actividades[act]["LF"] = max_tiempo

        for act in reversed(orden):
            data = actividades[act]

            sucesores = [
                s for s in actividades
                if act in actividades[s]["predecesores"]
            ]

            if not sucesores:
                LF = max_tiempo
            else:
                LF = min(actividades[s]["LS"] for s in sucesores)

            LS = LF - data["duracion"]

            data["LS"] = LS
            data["LF"] = LF

        # -------------------------
        # 7. RUTA CRÍTICA REAL (CAMINOS COMPLETOS)
        # -------------------------
        def es_critica(a, b):
            return (
                abs(actividades[a]["ES"] - actividades[a]["LS"]) < 1e-6 and
                abs(actividades[b]["ES"] - actividades[b]["LS"]) < 1e-6
            )

        sucesores = {
            a: [b for b in actividades if a in actividades[b]["predecesores"]]
            for a in actividades
        }

        inicios = [
            a for a in actividades
            if not actividades[a]["predecesores"]
            and abs(actividades[a]["LS"] - actividades[a]["ES"]) < 1e-6
        ]

        rutas = []

        def dfs(nodo, camino):
            camino.append(nodo)

            if not sucesores[nodo]:
                rutas.append(camino.copy())
                camino.pop()
                return

            for s in sucesores[nodo]:
                if es_critica(nodo, s):
                    dfs(s, camino)

            camino.pop()

        for i in inicios:
            dfs(i, [])

        ruta = max(
            rutas,
            key=lambda camino: sum(actividades[a]["duracion"] for a in camino)
        ) if rutas else []

        # -------------------------
        # 8. RESULTADO
        # -------------------------
        resultado = "Actividad | ES EF LS LF Holgura\n"
        resultado += "-" * 45 + "\n"

        for act, d in actividades.items():
            holgura = d["LS"] - d["ES"]
            resultado += f"{act:>3} | {d['ES']:>2} {d['EF']:>2} {d['LS']:>2} {d['LF']:>2} {holgura:>3}\n"

        resultado += "\nRuta crítica: " + " -> ".join(ruta)

        return resultado

    except Exception as e:
        return f"Error en PERT: {str(e)}"