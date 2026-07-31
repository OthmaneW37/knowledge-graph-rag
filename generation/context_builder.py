def build_graph_context(rows: list[dict]) -> str:
    if not rows:
        return ""

    lines = []
    for row in rows:
        lines.append(
            f"{row['source']} {row['relation']} {row['target']} (confidence={row['confidence']})"
        )

    return "\n".join(lines)


def build_vector_context(results: list[dict]) -> str:
    if not results:
        return ""

    return "\n".join([r["content"] for r in results])