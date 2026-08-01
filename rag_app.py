from retrieval.router import choose_retrieval_mode
from retrieval.graph_retriever import get_entity_relations
from retrieval.vector_retrieval import search_similar_chunks
from retrieval.entity_linker import extract_entity_from_question
from generation.context_builder import build_graph_context, build_vector_context
from generation.answer_generator import generate_answer


def ask_question(question: str) -> str:
    mode = choose_retrieval_mode(question)

    if mode == "graph":
        entity_name = extract_entity_from_question(question)
        if not entity_name:
            return "I could not identify a graph entity in the question."

        rows = get_entity_relations(entity_name)
        context = build_graph_context(rows)

    elif mode == "vector":
        results = search_similar_chunks(question)
        context = build_vector_context(results)

    else:
        entity_name = extract_entity_from_question(question)
        graph_context = ""

        if entity_name:
            rows = get_entity_relations(entity_name)
            graph_context = build_graph_context(rows)

        results = search_similar_chunks(question)
        vector_context = build_vector_context(results)

        context = f"{graph_context}\n\n{vector_context}".strip()

    return generate_answer(question, context)


if __name__ == "__main__":
    questions = [
        "What does PostgreSQL use?",
        "How is AuroraLearn connected to Zoom?",
        "Explain the platform architecture"
    ]

    for question in questions:
        print(f"\nQuestion: {question}")
        print("Answer:")
        print(ask_question(question))
        print("-" * 50)