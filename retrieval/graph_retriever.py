import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def get_driver():
    if not URI or not USERNAME or not PASSWORD:
        raise ValueError(
            "Missing Neo4j environment variables. Check NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD."
        )

    return GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


def list_entities(limit: int = 20) -> list[str]:
    driver = get_driver()

    query = """
    MATCH (e:Entity)
    RETURN e.name AS name
    LIMIT $limit
    """

    try:
        with driver.session(database=DATABASE) as session:
            result = session.run(query, limit=limit)
            return [record["name"] for record in result]
    finally:
        driver.close()


def get_entity_relations(entity_name: str) -> list[dict]:
    driver = get_driver()

    query = """
    MATCH (a:Entity)-[r]-(b:Entity)
    WHERE toLower(a.name) = toLower($entity_name)
    RETURN a.name AS source, r.relation_type AS relation, b.name AS target, r.confidence AS confidence
    """

    try:
        with driver.session(database=DATABASE) as session:
            result = session.run(query, entity_name=entity_name)
            return [record.data() for record in result]
    finally:
        driver.close()


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