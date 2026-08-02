import json
from pathlib import Path
from neo4j import GraphDatabase
from difflib import get_close_matches
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE

BASE_DIR = Path(__file__).resolve().parent.parent
FALLBACK_FILE = BASE_DIR / "retrieval" / "graph_cache.json"

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )
    return _driver


def get_all_entities():
    query = """
    MATCH (e:Entity)
    WHERE e.name IS NOT NULL
    RETURN e.name AS name
    """
    try:
        driver = get_driver()
        with driver.session(database=NEO4J_DATABASE) as session:
            results = session.run(query)
            return [record["name"] for record in results]
    except Exception as e:
        print(f"Warning: Neo4j connection failed in entity linker. Using local graph fallback. (Error: {e})")
        try:
            if FALLBACK_FILE.exists():
                with open(FALLBACK_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("entities", [])
        except Exception as fallback_error:
            print(f"Warning: Fallback failed to read in entity linker: {fallback_error}")
        return []


def extract_entity_from_question(question: str):
    entities = get_all_entities()
    if not entities:
        return None
        
    question_lower = question.lower()

    # Sort entities by length descending to match longer entities first (e.g. "programming interviews" before "interviews")
    sorted_entities = sorted(entities, key=len, reverse=True)

    for entity in sorted_entities:
        if entity.lower() in question_lower:
            return entity

    words = question.replace("?", "").replace(".", "").split()

    for word in words:
        matches = get_close_matches(word, sorted_entities, n=1, cutoff=0.8)
        if matches:
            return matches[0]

    return None


if __name__ == "__main__":
    entities = get_all_entities()
    print("Entities:", entities)
    print("Detected:", extract_entity_from_question("What does PostgreSQL use?"))
    print("Detected:", extract_entity_from_question("How is AuroraLearn connected to Zoom?"))