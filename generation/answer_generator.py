import requests

def call_ollama(prompt: str, model: str = "mistral:latest") -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=8,
    )
    response.raise_for_status()
    return response.json()["response"]


def generate_answer(question: str, context: str) -> str:
    if not context.strip():
        return "I could not find relevant information."

    prompt = f"""You are a helpful assistant. Answer the question using ONLY the context provided below. If you cannot answer it from the context, say you don't know. Keep your answer brief and direct.

Context:
{context}

Question: {question}
Answer:"""

    try:
        return call_ollama(prompt).strip()
    except Exception:
        # Graceful fallback when local Ollama model is not running
        return context