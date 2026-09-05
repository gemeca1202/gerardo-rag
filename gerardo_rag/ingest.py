from pathlib import Path
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import json

def extract_chunks(pdf_path, chunk_size=500):
    reader = PdfReader(str(pdf_path))
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"

    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size].strip()
        if len(chunk) > 50:
            chunks.append({"source": pdf_path.name, "text": chunk})
    return chunks

def build_index(pdf_paths):
    # Si le pasas 1 archivo o muchos, aquí lo arreglamos
    if not isinstance(pdf_paths, list):
        pdf_paths = [pdf_paths]

    print(f"Indexando: {[p.name for p in pdf_paths]}")

    all_records = []
    for pdf_path in pdf_paths:
        all_records.extend(extract_chunks(pdf_path))

    print(f"Fragmentos: {len(all_records)} - Generando embeddings locales...")

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    texts = [r["text"] for r in all_records]
    embeddings = model.encode(texts, show_progress_bar=True)

    for i, rec in enumerate(all_records):
        rec["embedding"] = embeddings[i].tolist()

    out_path = Path("data/processed/index.jsonl")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for r in all_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    return len(all_records)