import json
from embedder import embed_text

def save_embeddings(chunks: list[dict],output_file: str="vector_store.json"):
    records=[]

    for chunk in chunks:
        records.append({
            "chunk_id":chunk["chunk_id"],
            "content": chunk["content"],
            "position":chunk.get("position",0),
            "embedding":embed_text(chunk["content"]),
        })
    with open(output_file,"w",encoding="utf-8") as f:
        json.dump(records,f,ensure_ascii=False,indent=2)
    
if __name__=="__main__":
    sample_chunk=[
        {"chunk_id": "1", "content": "Kafka processes streaming events.", "position": 0},
        {"chunk_id": "2", "content": "Neo4j stores graph relationships.", "position": 1},
        {"chunk_id": "3", "content": "FraudIA detects fraud in real time.", "position": 2},
    ]

    save_embeddings(sample_chunk)
    print("vector_store.json created")