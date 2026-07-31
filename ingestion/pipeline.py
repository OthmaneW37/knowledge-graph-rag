from ingestion.chunker import chunk_document
from ingestion.extractor import extract_from_chunk
from ingestion.entity_resolver import resolve_entities
from ingestion.neo4j_writer import write_extraction
from indexing.local_vector_store import save_embeddings

def run_pipeline(text: str,chunk_size:int=100,overlap:int=20):
    chunks=chunk_document(text,chunk_size=chunk_size,overlap=overlap)

    for chunk in chunks:
        result=extract_from_chunk(chunk)
        result.entities=resolve_entities(result.entities)
        write_extraction(result)

    save_embeddings(chunks)
    return chunks

if __name__ == "__main__":
    sample_text="""
    AuroraLearn is an online platform that helps students prepare for programming interviews.

The company uses Python and JavaScript to build interactive coding challenges.

PostgreSQL stores user profiles, submissions, and progress data.

Redis is used to cache leaderboard information and session tokens.

The coaching team organizes weekly live sessions on algorithms and system design.

AuroraLearn integrates Zoom for live video, PostgreSQL for persistence, and Redis for fast access to frequently used data.
    """
    chunks=run_pipeline(sample_text)

    print(f"{len(chunks)} chunks processed and stored in Neo4j")