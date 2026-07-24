import os
import json 
import requests
from  typing import Literal
from pydantic import BaseModel,ValidationError
from dotenv import load_dotenv

load_dotenv()



EntityType = Literal["Company", "Person", "Technology", "Product", "Concept"]
RelationType = Literal["USES", "BUILDS", "WORKS_WITH", "MENTIONS", "RELATES_TO"]

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



def build_prompt(chunk_text:str,chunk_id:str)->str:
    return f""" 
    You are information extracion system

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

Rules :
-Use only these entity type :Company,Person,Technology,Product,Concept
-Use only these relation type :USES,BUILDS,WORKS_WITH,MENTIONS,RELATES_TO
-If nothing is found,return empty lists
-Do not add explanations
-The chunk_id for every relationship must be "{chunk_id}"

 Text: {chunk_text}"""


def call_ollama(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral:latest",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
    )
    response.raise_for_status()
    data = response.json()
    return data["response"]



def validate_relationships(result: ExtractionResult) -> ExtractionResult:
    entity_names = {e.name for e in result.entities}
    valid_relationships = [
        r for r in result.relationships
        if r.source in entity_names and r.target in entity_names
    ]
    result.relationships = valid_relationships
    return result

def extract_from_chunk(chunk:dict)->ExtractionResult:
    prompt=build_prompt(chunk["content"],chunk["chunk_id"])
    raw_output=call_ollama(prompt)
    data=json.loads(raw_output)
    parsed =ExtractionResult(**data)
    return validate_relationships(parsed)

if __name__ == "__main__":
    sample_chunk = {
        "chunk_id": "abc123",
        "content": "Kafka is used in FraudIA to process streaming fraud events.",
        "position": 0
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