from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = Path("data/processed/index.jsonl")
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

def load_index():
    records = []
    if not INDEX_PATH.exists():
        return []
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
    return records

def search(question, top_k=3):
    print(f"Buscando: {question} (100% local)...")
    records = load_index()
    if not records:
        print("No hay índice. Corre primero: py -m gerardo_rag.cli index")
        return []

    model = SentenceTransformer(MODEL_NAME)
    query_emb = model.encode([question])[0]

    # Convertir embeddings del índice a matriz
    index_embs = np.array([r["embedding"] for r in records])

    # Similitud coseno
    # Normalizamos
    query_norm = query_emb / np.linalg.norm(query_emb)
    index_norms = index_embs / np.linalg.norm(index_embs, axis=1, keepdims=True)
    scores = np.dot(index_norms, query_norm)

    # Top K
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for i in top_indices:
        results.append({
            "score": float(scores[i]),
            "text": records[i]["text"],
            "source": records[i]["source"]
        })
    return results