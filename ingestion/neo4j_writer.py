from httpcore import __name
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from extractor import ExtractionResult

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

driver= GraphDatabase.driver(URI,auth=AUTH)
driver.verify_connectivity()


def write_extraction(result: ExtractionResult):
    with driver.session(database=DATABASE) as session:
        for entity in result.entities:
            session.execute_write(
                lambda  tx: tx.run(
                    """
                    MERGE(e:Entity{name:$name,type:$type})
                    """,
                    name=entity.name,
                    type=entity.entity_type,
                )
            )

        for rel in result.relationships:
            session.execute_write(
                lambda tx: tx.run(
                    """
                    MATCH (source:Entity{name:$source_name})
                    MATCH (target:Entity{name:$target_name})
                    MERGE (source)-[r:RELATION {type :$relation_type}]->(target)
                    SET r.confidence = $confidence,
                    r.chunk_id=$chunk_id
                    """,
                    source_name=rel.source,
                    target_name=rel.target,
                    relation_type=rel.relation_type,
                    confidence=rel.confidence,
                    chunk_id=rel.chunk_id
                )
            )

if __name__ == "__main__":
    from extractor import Entity,Relationship,ExtractionResult

    sample = ExtractionResult(
        entities=[
            Entity(name="Kafka", entity_type="Technology"),
            Entity(name="FraudIA", entity_type="Product"),
        ],
        relationships=[
            Relationship(
                source="FraudIA",
                target="Kafka",
                relation_type="USES",
                confidence=0.95,
                chunk_id="abc123",
            )
        ]
    )

    write_extraction(sample)
    print("Written to Neo4j")
    