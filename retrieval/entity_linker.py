from neo4j import GraphDatabase
from difflib import get_close_matches
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)

def get_all_entities():
    query = """
    MATCH (e:Entity)
    WHERE e.name IS NOT NULL
    RETURN e.name AS name
    """

    with driver.session(database=NEO4J_DATABASE) as session:
        results = session.run(query)
        return [record["name"] for record in results]


def extract_entity_from_question(question: str):
    entities = get_all_entities()
    question_lower = question.lower()

    for entity in entities:
        if entity.lower() in question_lower:
            return entity

    words = question.replace("?", "").replace(".", "").split()

    for word in words:
        matches = get_close_matches(word, entities, n=1, cutoff=0.8)
        if matches:
            return matches[0]

    return None


if __name__ == "__main__":
    entities = get_all_entities()
    print("Entities:", entities)
    print("Detected:", extract_entity_from_question("What does PostgreSQL use?"))
    print("Detected:", extract_entity_from_question("How is AuroraLearn connected to Zoom?"))