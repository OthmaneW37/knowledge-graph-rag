import os
import json
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

BASE_DIR = Path(__file__).resolve().parent.parent
FALLBACK_FILE = BASE_DIR / "retrieval" / "graph_cache.json"

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        if not URI or not USERNAME or not PASSWORD:
            raise ValueError(
                "Missing Neo4j environment variables. Check NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD."
            )
        _driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    return _driver


def list_entities_fallback(limit: int = 20) -> list[str]:
    try:
        if FALLBACK_FILE.exists():
            with open(FALLBACK_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("entities", [])[:limit]
    except Exception as e:
        print(f"Warning: Fallback failed to read: {e}")
    return []


def get_entity_relations_fallback(entity_name: str) -> list[dict]:
    try:
        if FALLBACK_FILE.exists():
            with open(FALLBACK_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                relations = data.get("relationships", [])
                matched = []
                for r in relations:
                    if r["source"].lower() == entity_name.lower() or r["target"].lower() == entity_name.lower():
                        matched.append({
                            "source": r["source"],
                            "relation": r.get("relation") or r.get("relation_type") or "RELATES_TO",
                            "target": r["target"],
                            "confidence": r.get("confidence", 0.8)
                        })
                return matched
    except Exception as e:
        print(f"Warning: Fallback failed to read: {e}")
    return []


def list_entities(limit: int = 20) -> list[str]:
    query = """
    MATCH (e:Entity)
    RETURN e.name AS name
    LIMIT $limit
    """
    try:
        driver = get_driver()
        with driver.session(database=DATABASE) as session:
            result = session.run(query, limit=limit)
            return [record["name"] for record in result]
    except Exception as e:
        print(f"Warning: Neo4j connection failed. Using local graph fallback. (Error: {e})")
        return list_entities_fallback(limit)


def get_entity_relations(entity_name: str) -> list[dict]:
    query = """
    MATCH (a:Entity)-[r]-(b:Entity)
    WHERE toLower(a.name) = toLower($entity_name)
    RETURN a.name AS source, r.relation_type AS relation, b.name AS target, r.confidence AS confidence
    """
    try:
        driver = get_driver()
        with driver.session(database=DATABASE) as session:
            result = session.run(query, entity_name=entity_name)
            return [record.data() for record in result]
    except Exception as e:
        print(f"Warning: Neo4j connection failed. Using local graph fallback. (Error: {e})")
        return get_entity_relations_fallback(entity_name)


if __name__ == "__main__":
    entities = list_entities()
    print("Entities found:")
    print(entities)

    print("\nRelations for PostgreSQL:")
    rows = get_entity_relations("PostgreSQL")

    if not rows:
        print("No relations found for PostgreSQL.")
    else:
        for row in rows:
            print(row)