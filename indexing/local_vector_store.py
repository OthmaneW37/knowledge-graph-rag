import json
from pathlib import Path

from ingestion.chunker import chunk_document
from indexing.embedder import embed_text


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "indexing" / "vector_store.json"


def save_embeddings(chunks: list[dict], output_file: Path = OUTPUT_FILE) -> None:
    records = []

    for chunk in chunks:
        records.append(
            {
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "position": chunk["position"],
                "embedding": embed_text(chunk["content"]),
            }
        )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    input_file= BASE_DIR/"data"/"sample.txt"

    with open(input_file,"r", encoding="utf-8") as f:
        text =f.read()

    chunks = chunk_document(text, chunk_size=100, overlap=20)
    save_embeddings(chunks)

    print(f"{len(chunks)} chunks saved in {OUTPUT_FILE}")