def choose_retrieval_mode(question: str) -> str:
    q = question.lower()

    graph_keywords = [
        "relationship", "relationships", "connected",
        "uses", "use", "store", "stores",
        "linked", "between"
    ]

    hybrid_keywords = [
        "architecture", "how does", "how do", "explain",
        "workflow", "pipeline", "system"
    ]

    if any(word in q for word in hybrid_keywords):
        return "hybrid"

    if any(word in q for word in graph_keywords):
        return "graph"

    return "vector"


if __name__ == "__main__":
    print(choose_retrieval_mode("What does PostgreSQL store?"))
    print(choose_retrieval_mode("Explain the platform architecture"))