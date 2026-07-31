def generate_answer(question: str, context: str) -> str:
    if not context.strip():
        return "I could not find relevant information."

    return context