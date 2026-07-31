from retrieval.router import choose_retrieval_mode
from retrieval.graph_retriever import get_entity_relations
from retrieval.vector_retrieval import search_similar_chunks
from generation.context_builder import build_graph_context, build_vector_context
from generation.answer_generator import generate_answer


def ask_question(question: str) -> str:
    mode = choose_retrieval_mode(question)

    if mode == "graph":
        rows = get_entity_relations("PostgreSQL")
        context = build_graph_context(rows)

    elif mode == "vector":
        results = search_similar_chunks(question)
        context = build_vector_context(results)

    else:  
        rows = get_entity_relations("AuroraLearn")
        graph_context = build_graph_context(rows)

        results = search_similar_chunks(question)
        vector_context = build_vector_context(results)

        context = f"Graph context:\n{graph_context}\n\nVector context:\n{vector_context}"

    return generate_answer(question, context)


if __name__ == "__main__":
    question = "Explain the platform architecture"
    answer = ask_question(question)
    print(answer)