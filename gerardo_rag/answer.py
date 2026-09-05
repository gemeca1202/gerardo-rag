import requests
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"

def answer_question(question, results):
    if not results:
        return "No encontré nada en tu CV."
    context = "\n\n".join([f"- {r['text']}" for r in results])
    prompt = f"""Eres el asistente de Gerardo Mena Castillo. Responde usando SOLO este contexto de su CV:
CONTEXTO:
{context}
PREGUNTA: {question}
Responde en español, en 1ra persona como si fueras Gerardo, profesional y breve.
"""
    print("\n=== GENERANDO CON OLLAMA LOCAL ===\n")
    try:
        resp = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=120)
        return resp.json()['response']
    except Exception as e:
        return f"Error con Ollama: {e}\n\nContexto crudo:\n{context[:2000]}"