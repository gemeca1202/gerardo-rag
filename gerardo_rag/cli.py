from __future__ import annotations

import argparse
import os
from pathlib import Path

from .answer import answer_question
from .config import DEFAULT_CV_NAME, RAW_DIR, load_settings
from .ingest import build_index
from .search import search


def require_key() -> None:
    key = os.getenv("OPENAI_API_KEY", "")
    if not key or key == "pon_tu_clave_aqui" or not key.startswith("sk-"):
        raise SystemExit("Falta OPENAI_API_KEY. Copia .env.example a .env y agrega tu clave.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerardo-RAG: consulta el CV ejecutivo de Gerardo.")
    subcommands = parser.add_subparsers(dest="command", required=True)
    index = subcommands.add_parser("index", help="Extrae, fragmenta y vectoriza uno o más PDFs.")
    index.add_argument(
        "--files",
        type=Path,
        nargs="+",
        help="PDFs específicos que se incorporarán. Si se omite, usa todos los PDF de data/raw.",
    )
    ask = subcommands.add_parser("ask", help="Recupera contexto y genera una respuesta.")
    ask.add_argument("question")
    ask.add_argument("--top-k", type=int, default=4)
    ask.add_argument("--show-context", action="store_true")
    args = parser.parse_args()

    load_settings()
    require_key()
    if args.command == "index":
        files = args.files or sorted(RAW_DIR.glob("*.pdf"))
        missing = [str(path) for path in files if not path.exists()]
        if missing:
            raise SystemExit("No encontré: " + ", ".join(missing))
        if not files:
            raise SystemExit(f"No encontré PDFs en: {RAW_DIR}")
        print("Indexando: " + ", ".join(path.name for path in files))
        print(f"Listo: {build_index(files)} fragmentos guardados en data/processed/index.jsonl")
        return

    results = search(args.question, args.top_k)
    if args.show_context:
        print("\n--- Contexto recuperado ---")
        for result in results:
            meta = result["metadata"]
            print(f"\n{meta['source']} | página {meta['page']} | similitud {result['score']:.3f}\n{result['text']}")
    print("\n--- Respuesta ---")
    print(answer_question(args.question, results))


if __name__ == "__main__":
    main()
