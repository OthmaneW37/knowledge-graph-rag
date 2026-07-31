from retrieval.router import choose_retrieval_mode
from retrieval.graph_retriever import get_entity_relations
from retrieval.vector_retrieval import search_similar_chunks
from generation.context_builder import build_graph_context, build_vector_context
from generation.answer_generator import generate_answer


def ask_question(question: str) -> str:
    mode = choose_retrieval_mode(question)

    if mode == "graph":
        entity_name = "PostgreSQL"   # temporaire pour test
        rows = get_entity_relations(entity_name)
        context = build_graph_context(rows)
    else:
        results = search_similar_chunks(question)
        context = build_vector_context(results)

    return generate_answer(question, context)


if __name__ == "__main__":
    question = "What does PostgreSQL store?"
    print(ask_question(question))