from __future__ import annotations

import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_PDF = BASE_DIR / "data" / "Investigacion-Operaciones10Edicion-Frederick-S-Hillier.pdf"


def _normalizar_texto(texto: str) -> str:
    return re.sub(r"\s+", " ", texto.lower()).strip()


def _tokenizar(texto: str) -> list[str]:
    return re.findall(r"[a-záéíóúñ0-9]+", texto.lower())


@lru_cache(maxsize=1)
def cargar_fragmentos_libro(ruta_pdf: str | None = None) -> list[tuple[int, str]]:
    path = Path(ruta_pdf) if ruta_pdf else DEFAULT_PDF

    if not path.exists():
        return []

    lector = PdfReader(str(path))
    fragmentos: list[tuple[int, str]] = []

    for numero_pagina, pagina in enumerate(lector.pages, start=1):
        texto = pagina.extract_text() or ""
        texto = _normalizar_texto(texto)
        if not texto:
            continue

        tamano = 1400
        solapamiento = 250
        inicio = 0

        while inicio < len(texto):
            fragmento = texto[inicio : inicio + tamano].strip()
            if fragmento:
                fragmentos.append((numero_pagina, fragmento))
            if inicio + tamano >= len(texto):
                break
            inicio += tamano - solapamiento

    return fragmentos


def buscar_contexto_libro(pregunta: str, max_fragmentos: int = 3) -> str:
    fragmentos = cargar_fragmentos_libro()
    if not fragmentos:
        return ""

    tokens_pregunta = Counter(_tokenizar(pregunta))
    if not tokens_pregunta:
        return ""

    puntuados: list[tuple[int, int, str]] = []

    for pagina, fragmento in fragmentos:
        tokens_fragmento = Counter(_tokenizar(fragmento))
        puntuacion = sum(min(tokens_pregunta[token], tokens_fragmento[token]) for token in tokens_pregunta)

        if puntuacion > 0:
            puntuados.append((puntuacion, pagina, fragmento))

    if not puntuados:
        return ""

    puntuados.sort(key=lambda item: item[0], reverse=True)
    seleccionados = puntuados[:max_fragmentos]

    lineas = ["Contexto relevante del libro de IO:"]

    for puntuacion, pagina, fragmento in seleccionados:
        resumen = fragmento[:700].strip()
        if len(fragmento) > 700:
            resumen += "..."
        lineas.append(f"[Página {pagina}] {resumen}")

    return "\n".join(lineas)