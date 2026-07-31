from fastapi import FastAPI
from pydantic import BaseModel
from rag_app import ask_question
from retrieval.router import choose_retrieval_mode

app = FastAPI(title="Knowledge Graph RAG API")

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    question: str
    mode: str
    answer: str

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/ask", response_model=QuestionResponse)
def ask(payload: QuestionRequest):
    mode = choose_retrieval_mode(payload.question)
    answer = ask_question(payload.question)

    return QuestionResponse(
        question=payload.question,
        mode=mode,
        answer=answer
    )