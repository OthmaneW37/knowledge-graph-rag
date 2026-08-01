from rag_app import ask_question


def load_questions(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def run_evaluation():
    questions = load_questions("eval/eval_questions.txt")

    print("=" * 60)
    print("RAG EVALUATION")
    print("=" * 60)

    for i, question in enumerate(questions, start=1):
        answer = ask_question(question)

        print(f"\n[{i}] Question: {question}")
        print("Answer:")
        print(answer)
        print("-" * 60)


if __name__ == "__main__":
    run_evaluation()