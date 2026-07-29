from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str) -> list[float]:
    return model.encode(text).tolist()

if __name__ == "__main__":
    vec = embed_text("Kafka is used in FraudIA to process streaming fraud events.")
    print("Dimension:", len(vec))
    print("First 5 values:", vec[:5])