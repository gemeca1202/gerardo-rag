from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
INDEX_PATH = PROCESSED_DIR / "index.jsonl"
MANIFEST_PATH = PROCESSED_DIR / "manifest.json"

# Cargarlo aquí hace que los módulos de ingesta y consulta vean los valores
# configurados antes de definir sus constantes.
load_dotenv(ROOT / ".env")

DEFAULT_CV_NAME = "CV_EJECUTIVO_GERARDO_MENA.pdf"
EMBEDDING_MODEL = os.getenv("GERARDO_RAG_EMBEDDING_MODEL", "text-embedding-3-small")
ANSWER_MODEL = os.getenv("GERARDO_RAG_ANSWER_MODEL", "gpt-5-mini")


def load_settings() -> None:
    """Recarga .env por si la aplicación se integra desde otro punto de entrada."""
    load_dotenv(ROOT / ".env")
