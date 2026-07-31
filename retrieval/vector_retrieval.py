import json
from pathlib import Path

import numpy as np

from indexing.embedder import embed_text


BASE_DIR = Path(__file__).resolve().parent.parent
STORE_FILE = BASE_DIR / "indexing" / "vector_store.json"


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def search_similar_chunks(
    query: str,
    top_k: int = 3,
    store_file: Path = STORE_FILE,
) -> list[dict]:
    query_embedding = np.array(embed_text(query))

    with open(store_file, "r", encoding="utf-8") as f:
        records = json.load(f)

    scored = []

    for record in records:
        chunk_embedding = np.array(record["embedding"])
        score = cosine_similarity(query_embedding, chunk_embedding)

        scored.append(
            {
                "chunk_id": record["chunk_id"],
                "content": record["content"],
                "position": record["position"],
                "score": score,
            }
        )

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    query = "Which tool manages graph relationships?"
    results = search_similar_chunks(query)

    for result in results:
        print(result["chunk_id"], result["score"], "->", result["content"])