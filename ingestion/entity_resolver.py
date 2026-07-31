from ingestion.extractor import Entity


def normalize_entity_name(name: str) -> str:
    return " ".join(name.strip().split())


def resolve_entities(entities: list[Entity]) -> list[Entity]:
    resolved = {}

    for entity in entities:
        canonical_name = normalize_entity_name(entity.name)
        key = (canonical_name.lower(), entity.entity_type)

        if key not in resolved:
            resolved[key] = Entity(
                name=canonical_name,
                entity_type=entity.entity_type
            )

    return list(resolved.values())


if __name__ == "__main__":
    entities = [
        Entity(name=" PostgreSQL ", entity_type="Technology"),
        Entity(name="postgresql", entity_type="Technology"),
        Entity(name="AuroraLearn", entity_type="Company"),
        Entity(name=" auroraLearn ", entity_type="Company"),
        Entity(name="leaderboard information", entity_type="Concept")
    ]

    resolved = resolve_entities(entities)

    for entity in resolved:
        print(entity)