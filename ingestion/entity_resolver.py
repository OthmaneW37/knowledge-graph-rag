from extractor import Entity

def normalize_entity_name(name :str) -> str:
    name = name.strip()
    name = "".join(name.split())
    return name.title()

def resolve_entities(entities :list[Entity]) -> list[Entity]:
    resolved={}

    for entity in entities:
        canonical_name=normalize_entity_name(entity.name)

        key=(canonical_name,entity.entity_type)

        if key not in resolved:
            resolved[key]=Entity(
                name=canonical_name,
                entity_type=entity.entity_type
            )

    return list(resolved.values())


if __name__=="__main__":
    entities=[
        Entity(name=" kafka ", entity_type="Technology"),
        Entity(name="Kafka", entity_type="Technology"),
        Entity(name="KAFKA", entity_type="Technology"),
        Entity(name="FraudIA", entity_type="Product")
    ]

    resolved= resolve_entities(entities)

    for entity in resolved:
        print(entity)