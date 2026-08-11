# Knowledge Graph RAG

Hybrid Retrieval-Augmented Generation project combining **knowledge-graph retrieval** and **semantic vector search** to build more grounded LLM answers.

## Why this project

Classic vector RAG is effective for semantic similarity, but it can struggle with explicit relationships between entities. This project explores a hybrid approach:

- **Graph retrieval** for entities and relationships
- **Vector retrieval** for semantic similarity
- **Hybrid mode** when a question benefits from both
- **LLM generation** over the retrieved context

## Architecture

```text
User question
     |
     v
Retrieval router
  /      |       \
Graph  Vector   Hybrid
  \      |       /
   Context builder
         |
         v
   LLM answer generation
```

The main application routes each question through the appropriate retrieval strategy, builds a unified context, and passes it to the answer-generation layer.

## Main components

```text
knowledge-graph-rag/
├── ingestion/      # Data ingestion pipeline
├── indexing/       # Index construction
├── retrieval/      # Graph, vector and hybrid retrieval logic
├── generation/     # Context building and answer generation
├── eval/           # Evaluation utilities
├── api.py          # API entry point
├── rag_app.py      # RAG orchestration
├── main.py         # Main application entry point
└── config.py       # Environment-based configuration
```

## Tech stack

- **Python**
- **Neo4j** for graph-based retrieval
- **Vector search** for semantic retrieval
- **LLM-based generation**
- Environment-based configuration with `python-dotenv`

## Retrieval flow

The application supports three retrieval modes:

1. **Graph** — identifies an entity, retrieves its relations, then builds graph context.
2. **Vector** — retrieves semantically similar chunks and builds vector context.
3. **Hybrid** — combines graph relations with semantic vector results before generation.

A simplified version of the orchestration is implemented in `rag_app.py`.

## Configuration

Create a local `.env` file from `.env.example` and configure your Neo4j instance:

```env
NEO4J_URI=neo4j://127.0.0.1:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
```

Never commit real credentials to the repository.

## Example questions

```text
How is entity A connected to entity B?
What technologies are related to a given platform?
Explain the architecture using both semantic context and graph relationships.
```

## What this project demonstrates

- Knowledge graph integration in a RAG pipeline
- Semantic and graph-based retrieval strategies
- Retrieval routing
- Context construction for LLMs
- Modular Python architecture for GenAI applications

## Roadmap

- Add reproducible evaluation metrics
- Improve entity linking
- Add reranking for semantic retrieval
- Add citations / source tracing in generated answers
- Add automated tests and deployment documentation

---

Built as an applied **GraphRAG / Generative AI** project focused on combining structured relationships with semantic search.
