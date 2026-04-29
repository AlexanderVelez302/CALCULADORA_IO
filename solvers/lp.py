import re
from pulp import (
    LpBinary,
    LpContinuous,
    LpInteger,
    LpMaximize,
    LpMinimize,
    LpProblem,
    LpStatus,
    LpVariable,
    PULP_CBC_CMD,
    lpSum,
)


def _normalizar(texto):
    return (
        texto.lower()
        .replace("−", "-")
        .replace("–", "-")
        .replace("—", "-")
    )


def _extraer_terminos_lineales(expresion):
    expresion = expresion.replace(" ", "")
    terminos = re.findall(r'([+-]?(?:\d+(?:\.\d+)?)?)\s*([a-z]\w*)', expresion)

    coeficientes = {}
    variables = []

    for coef_texto, variable in terminos:
        if variable not in coeficientes:
            variables.append(variable)

        if coef_texto in ("", "+"):
            coef = 1.0
        elif coef_texto == "-":
            coef = -1.0
        else:
            coef = float(coef_texto)

        coeficientes[variable] = coeficientes.get(variable, 0.0) + coef

    return coeficientes, variables


def _extraer_objetivo(texto):
    for linea in texto.splitlines():
        linea_norm = _normalizar(linea)
        if re.search(r'\bmax(?:imizar)?\b|\bmin(?:imizar)?\b', linea_norm):
            if "=" not in linea_norm:
                continue

            tipo = "max" if "max" in linea_norm else "min"
            expresion = linea_norm.split("=", 1)[1].strip()
            expresion = re.split(r'\b(?:restricciones?|sujeto a|subject to)\b', expresion)[0].strip()
            return tipo, expresion

    return None, None


def _extraer_restricciones(texto):
    restricciones = []

    for linea in texto.splitlines():
        linea_norm = _normalizar(linea)
        if re.search(r'\bmax(?:imizar)?\b|\bmin(?:imizar)?\b', linea_norm):
            continue
        if not any(op in linea_norm for op in ("<=", ">=", "=")):
            continue

        operador = None
        for op in ("<=", ">=", "="):
            if op in linea_norm:
                operador = op
                izquierda, derecha = linea_norm.split(op, 1)
                break

        if not operador:
            continue

        izquierda = re.sub(r'^\s*\d+\.?\s*', '', izquierda).strip()
        derecha = re.split(r'\s*\([^)]*\)\s*$', derecha.strip())[0].strip()

        valor_match = re.search(r'[-+]?\d+(?:[\.,]\d+)?', derecha)
        if not valor_match:
            continue

        rhs = float(valor_match.group(0).replace(',', '.'))
        restricciones.append((izquierda, operador, rhs))

    return restricciones


def _detectar_modo_variables(texto):
    texto_norm = _normalizar(texto)

    if re.search(r'\b(binaria|binario|binarias|binarios|0-1|booleana|booleano)\b', texto_norm):
        return "binary"

    if re.search(r'\b(entera|enteras|entero|enteros|integer|integral)\b', texto_norm):
        return "integer"

    if re.search(r'\b(unidades|equipos|máquinas|maquinas|personas|vehículos|vehiculos|camiones|productos|lotes|artículos|articulos|piezas)\b', texto_norm):
        return "integer"

    return "continuous"


def _detectar_categoria_variable(texto, variable, modo_global):
    texto_norm = _normalizar(texto)
    patron_variable = rf'\b{re.escape(variable)}\b'

    clausulas = [segmento.strip() for segmento in re.split(r'[;\n\r]+|\s*,\s*', texto_norm) if segmento.strip()]

    for clausula in clausulas:
        if not re.search(patron_variable, clausula):
            continue

        if re.search(r'\b(?:binaria|binario|binarias|binarios|0-1|booleana|booleano)\b', clausula):
            return LpBinary, "binary"

        if re.search(r'\b(?:entera|enteras|entero|enteros|integer|integral)\b', clausula):
            return LpInteger, "integer"

    if modo_global == "binary":
        return None

    if modo_global == "integer":
        return None

    return LpContinuous, "continuous"


def parsear_lp(texto):
    texto_norm = _normalizar(texto)

    tipo_objetivo, objetivo = _extraer_objetivo(texto_norm)
    if not objetivo:
        return None

    restricciones_raw = _extraer_restricciones(texto_norm)
    if not restricciones_raw:
        return None

    coef_objetivo, variables_objetivo = _extraer_terminos_lineales(objetivo)

    variables = list(variables_objetivo)
    for lhs, _, _ in restricciones_raw:
        _, vars_lhs = _extraer_terminos_lineales(lhs)
        for variable in vars_lhs:
            if variable not in variables:
                variables.append(variable)

    if not variables:
        return None

    modo_global = _detectar_modo_variables(texto_norm)

    categorias_explicitas = {
        variable: _detectar_categoria_variable(texto_norm, variable, modo_global)
        for variable in variables
    }

    hay_categorias_explicitas = any(valor is not None for valor in categorias_explicitas.values())

    categorias_variables = {}
    for variable in variables:
        categoria = categorias_explicitas[variable]
        if categoria is None:
            if modo_global == "binary":
                categoria = (LpBinary, "binary") if not hay_categorias_explicitas else (LpContinuous, "continuous")
            elif modo_global == "integer":
                categoria = (LpInteger, "integer") if not hay_categorias_explicitas else (LpContinuous, "continuous")
            else:
                categoria = (LpContinuous, "continuous")

        categorias_variables[variable] = categoria

    c_original = [coef_objetivo.get(variable, 0.0) for variable in variables]
    c = [-valor for valor in c_original] if tipo_objetivo == "max" else c_original

    A_ub = []
    b_ub = []
    A_eq = []
    b_eq = []

    for lhs, operador, rhs in restricciones_raw:
        coef_lhs, _ = _extraer_terminos_lineales(lhs)
        fila = [coef_lhs.get(variable, 0.0) for variable in variables]

        if operador == "<=":
            A_ub.append(fila)
            b_ub.append(rhs)
        elif operador == ">=":
            A_ub.append([-valor for valor in fila])
            b_ub.append(-rhs)
        else:
            A_eq.append(fila)
            b_eq.append(rhs)

    return c_original, A_ub, b_ub, A_eq, b_eq, variables, tipo_objetivo, categorias_variables


def resolver_lp(pregunta):
    try:
        data = parsear_lp(pregunta)

        if not data:
            return "⚠️ No se pudo interpretar el problema de LP"

        c_original, A_ub, b_ub, A_eq, b_eq, variables, tipo_objetivo, categorias_variables = data

        sentido = LpMaximize if tipo_objetivo == "max" else LpMinimize
        problema = LpProblem("LP_Automatico", sentido)

        variables_lp = {
            variable: LpVariable(variable, lowBound=0, cat=categorias_variables[variable][0])
            for variable in variables
        }

        problema += lpSum(c_original[i] * variables_lp[variable] for i, variable in enumerate(variables))

        for fila, rhs in zip(A_ub, b_ub):
            problema += lpSum(coef * variables_lp[variable] for coef, variable in zip(fila, variables)) <= rhs

        for fila, rhs in zip(A_eq, b_eq):
            problema += lpSum(coef * variables_lp[variable] for coef, variable in zip(fila, variables)) == rhs

        problema.solve(PULP_CBC_CMD(msg=False))

        if LpStatus[problema.status] == "Optimal":
            valores = {variable: variables_lp[variable].value() or 0.0 for variable in variables}
            z = problema.objective.value() or 0.0

            lineas_resultado = ["📌 RESULTADO ÓPTIMO"]
            for variable in variables:
                lineas_resultado.append(f"{variable} = {valores[variable]:.2f}")
            lineas_resultado.append(f"Z = {z:.2f}")
            tipos_resumen = {categoria for _, categoria in categorias_variables.values()}
            tipo_texto = "mixed" if len(tipos_resumen) > 1 else next(iter(tipos_resumen))
            lineas_resultado.append(f"Tipo de variables: {tipo_texto}")

            return "\n".join(lineas_resultado)

        return f"❌ No óptimo: {LpStatus[problema.status]}"

    except Exception as e:
        return f"❌ Error en LP: {e}"