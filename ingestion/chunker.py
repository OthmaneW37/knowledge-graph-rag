import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_document(text: str,chunk_size: int,overlap: int) -> list[dict]:
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        is_separator_regex=False,
    )
    raw_chunks=splitter.split_text(text)
    chunks=[]

    for i,chunk in enumerate(raw_chunks):
        chunk_id=hashlib.md5(chunk.encode("utf-8")).hexdigest()
        chunks.append({
            "chunk_id": chunk_id,
            "content":chunk,
            "position":i
            })

    return chunks
    

if __name__=="__main__":
        sample_text="""
        Fraud detection systems often rely on streaming architectures.
        Kafka is used to ingest events in real time.
        Neo4j can model relationships between customers, merchants, and devices.
        Pgvector can store embeddings for semantic retrieval.
        """
        chunks =chunk_document(sample_text,chunk_size=100,overlap=20)

        for chunk in chunks :
            print(chunk)
            print("-"*40)    
    