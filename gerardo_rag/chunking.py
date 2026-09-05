from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    """Un fragmento autocontenido y trazable que se puede recuperar."""

    text: str
    page: int
    chunk_number: int


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def chunk_page(text: str, page: int, size: int = 180, overlap: int = 35) -> list[TextChunk]:
    """Corta una página por palabras, reteniendo solapamiento entre trozos.

    El solapamiento evita que una idea que cae justo en un corte pierda su
    contexto. El tamaño es deliberadamente pequeño para un CV: cada resultado
    suele corresponder a una experiencia, logro o sección concreta.
    """
    if size <= overlap:
        raise ValueError("size debe ser mayor que overlap")
    words = normalize_text(text).split()
    chunks: list[TextChunk] = []
    start = 0
    number = 1
    while start < len(words):
        window = words[start : start + size]
        if not window:
            break
        chunks.append(TextChunk(" ".join(window), page, number))
        if start + size >= len(words):
            break
        start += size - overlap
        number += 1
    return chunks
