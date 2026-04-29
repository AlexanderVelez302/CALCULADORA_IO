import re

from groq import Groq
import os

from ai.embeddings import buscar_contexto_libro

_groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=_groq_api_key) if _groq_api_key else None


def _es_resultado_pert(resultado):
    return "Actividad | ES EF LS LF Holgura" in resultado and "Ruta crítica:" in resultado


def _explicar_pert(resultado):
    ruta_match = re.search(r"Ruta crítica:\s*(.+)", resultado)
    ruta = ruta_match.group(1).strip() if ruta_match else ""

    actividades_no_criticas = []
    duracion_total = 0
    for linea in resultado.splitlines():
        match = re.match(r"\s*([A-Z])\s*\|\s*\d+\s+\d+\s+\d+\s+\d+\s+(-?\d+)", linea)
        if not match:
            continue
        actividad = match.group(1)
        valores = re.findall(r"\d+", linea)
        if len(valores) >= 2:
            duracion_total = max(duracion_total, int(valores[1]))
        holgura = int(match.group(2))
        if holgura > 0:
            actividades_no_criticas.append(f"{actividad} (holgura {holgura})")

    partes = [
        "**Fuente consultada:** Libro de Investigación de Operaciones (Hillier)",
        "**Tipo de problema:** Red de actividades con ruta crítica",
        "**Método usado:** Tabla ES/EF/LS/LF y cálculo de holguras",
        "**Interpretación del resultado:**",
    ]

    if ruta:
        partes.append(f"- La ruta crítica es {ruta}, por lo que esas actividades no admiten retraso.")

    if duracion_total:
        partes.append(f"- La duración total del proyecto es de {duracion_total} días.")

    if actividades_no_criticas:
        partes.append(
            "- No son críticas: " + ", ".join(actividades_no_criticas) + "."
        )

    partes.append("- Las actividades críticas tienen holgura 0, así que cualquier atraso en ellas retrasa el proyecto.")
    return "\n\n".join(partes)


def explicar_con_ia(pregunta, resultado):
    try:
        if _es_resultado_pert(resultado):
            return _explicar_pert(resultado)

        if client is None:
            return "⚠️ No hay clave GROQ_API_KEY configurada para generar la explicación IA."

        contexto_libro = buscar_contexto_libro(pregunta)

        prompt = f"""
Eres un profesor experto en Investigación de Operaciones.

Explica como si estuvieras calificando un examen, no escribiendo un artículo.

Tu tarea es explicar ejercicios de forma CLARA, CORTA y TIPO EXAMEN.

REGLAS OBLIGATORIAS:
- Máximo 8 a 12 líneas
- Nada de texto innecesario
- No escribir párrafos largos
- Usar viñetas si es necesario
- Explicar SOLO lo importante
- Enfocarte en método + interpretación
- Estilo profesor universitario

FORMATO:

0. Fuente consultada
1. Tipo de problema
2. Método usado
3. Interpretación del resultado (muy claro)

REGLAS PARA NO EQUIVOCARTE:
- Basa tu explicación SOLO en el resultado calculado.
- Si una actividad tiene holgura mayor que 0, NO la llames crítica.
- Si ya aparece una ruta crítica, úsala exactamente como está escrita.
- No inventes relaciones de precedencia ni actividades "críticas en sí mismas" si no están en la ruta crítica.
- No contradigas la tabla ES/EF/LS/LF.
- Si usas contexto del libro, menciónalo como fuente consultada.

PROBLEMA:
{pregunta}

{contexto_libro}

RESULTADO:
{resultado}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Eres un profesor estricto de IO, claro y directo."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        contenido = response.choices[0].message.content
        if contexto_libro:
            return f"**Fuente consultada:** Libro de Investigación de Operaciones (Hillier)\n\n{contenido}"

        return contenido

    except Exception as e:
        return f"⚠️ Error IA: {e}"