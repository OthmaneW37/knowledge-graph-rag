import json
import requests
from typing import Literal
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv

load_dotenv()

EntityType = Literal["Company", "Person", "Technology", "Product", "Concept"]
RelationType = Literal["USES", "BUILDS", "WORKS_WITH", "MENTIONS", "RELATES_TO", "STORES"]


ALLOWED_RELATIONS = {"USES", "BUILDS", "WORKS_WITH", "MENTIONS", "RELATES_TO", "STORES"}

RELATION_MAPPING = {
    "USES": "USES",
    "BUILDS": "BUILDS",
    "WORKS_WITH": "WORKS_WITH",
    "MENTIONS": "MENTIONS",
    "RELATES_TO": "RELATES_TO",
    "STORES": "STORES",
    "INTEGRATES": "WORKS_WITH",
    "CONNECTS": "WORKS_WITH",
    "LINKS": "WORKS_WITH",
    "DEPENDS_ON": "RELATES_TO",
    "SUPPORTS": "RELATES_TO",
    "MANAGES": "RELATES_TO",
    "PROVIDES": "RELATES_TO",
}


class Entity(BaseModel):
    name: str
    entity_type: EntityType


class Relationship(BaseModel):
    source: str
    target: str
    relation_type: RelationType
    confidence: float
    chunk_id: str


class ExtractionResult(BaseModel):
    entities: list[Entity]
    relationships: list[Relationship]


def build_prompt(chunk_text: str, chunk_id: str) -> str:
    return f"""
You are an information extraction system.

Extract entities and relationships from the text below.

Return ONLY valid JSON with this structure:

{{
  "entities": [
    {{"name": "example", "entity_type": "Technology"}}
  ],
  "relationships": [
    {{
      "source": "example source",
      "target": "example target",
      "relation_type": "USES",
      "confidence": 0.95,
      "chunk_id": "{chunk_id}"
    }}
  ]
}}

Rules:
- Use only these entity types: Company, Person, Technology, Product, Concept
- Use only these relation types: USES, BUILDS, WORKS_WITH, MENTIONS, RELATES_TO, STORES
- If a relationship does not clearly match one of these, use RELATES_TO
- If nothing is found, return empty lists
- Do not add explanations
- The chunk_id for every relationship must be "{chunk_id}"

Text:
{chunk_text}
"""


def call_ollama(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral:latest",
            "prompt": prompt,
            "stream": False,
            "format": "json",
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["response"]


def normalize_relation_type(value: str) -> str:
    if not value:
        return "RELATES_TO"

    value = value.strip().upper()
    value = RELATION_MAPPING.get(value, value)

    if value not in ALLOWED_RELATIONS:
        return "RELATES_TO"

    return value


def normalize_extraction_data(data: dict, chunk_id: str) -> dict:
    data.setdefault("entities", [])
    data.setdefault("relationships", [])

    for rel in data["relationships"]:
        rel["relation_type"] = normalize_relation_type(rel.get("relation_type"))
        rel["chunk_id"] = chunk_id

        if "confidence" not in rel or rel["confidence"] is None:
            rel["confidence"] = 0.8

    return data


def validate_relationships(result: ExtractionResult) -> ExtractionResult:
    entity_names = {e.name for e in result.entities}

    valid_relationships = [
        r for r in result.relationships
        if r.source in entity_names and r.target in entity_names
    ]

    result.relationships = valid_relationships
    return result


def extract_from_chunk(chunk: dict) -> ExtractionResult:
    prompt = build_prompt(chunk["content"], chunk["chunk_id"])
    raw_output = call_ollama(prompt)
    data = json.loads(raw_output)
    data = normalize_extraction_data(data, chunk["chunk_id"])
    parsed = ExtractionResult(**data)
    return validate_relationships(parsed)


if __name__ == "__main__":
    sample_chunk = {
        "chunk_id": "abc123",
        "content": "AuroraLearn integrates Zoom, PostgreSQL, and Redis into its online learning platform.",
        "position": 0,
    }

    try:
        result = extract_from_chunk(sample_chunk)
        print(result.model_dump_json(indent=2))
    except ValidationError as e:
        print("Validation error:")
        print(e)
    except Exception as e:
        print("Other error:")
        print(e)