# Multi-Agent System

A multi-agent AI assistant built with **LangGraph**. A supervisor agent decides, step by step, whether to answer from a private knowledge base (RAG), search the web, analyze what was gathered, or write the final answer. Answers stream to a React UI over Server-Sent Events.

## Architecture

```
                    ┌────────────┐
   user request ──▶ │ supervisor │ ◀───────────┐
                    └─────┬──────┘             │
          ┌───────────────┼───────────────┐    │
          ▼               ▼               ▼    │
     ┌────────┐     ┌──────────┐     ┌──────────┐
     │  rag   │     │ research │     │ analysis │
     └───┬────┘     └────┬─────┘     └────┬─────┘
         └───────────────┴──▶ supervisor   │
                                           ▼
                                      ┌─────────┐
                                      │  final  │ ──▶ streamed answer
                                      └─────────┘
```

- **supervisor**: structured-output router (Gemini). Picks the next agent, with a hard step limit (`MAX_STEPS = 5`).
- **rag**: hybrid retrieval over the indexed documents, followed by an answer with citations.
- **research**: web search through Tavily.
- **analysis**: compares and filters what RAG and research found.
- **final**: writes the answer from the collected context and streams tokens.

### RAG pipeline

```
files ─▶ load ─▶ clean ─▶ metadata ─▶ chunk (1000 / 150 overlap)
      ─▶ embed (multilingual MiniLM) ─▶ FAISS
query ─▶ FAISS (k=20) + BM25 (k=20) ─▶ ensemble ─▶ Cohere rerank (top 5) ─▶ LLM
```

If the reranker call fails, retrieval falls back to the plain hybrid results.

Supported inputs: `.pdf`, `.docx`, `.txt`, `.md`.

## Project layout

```
agents/      supervisor, rag / research / analysis / final agents, graph
app/         FastAPI service (chat + streaming endpoints)
rag/         ingestion, chunking, embedding, vector store, retrieval, generation
tools/       tools used by the agents
frontend/    React + Vite chat UI
main.py      terminal chat
```

## Setup

Requires Python 3.10+ and Node 18+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_key
GOOGLE_API_KEY=your_key      # set this too if langchain-google-genai does not pick up GEMINI_API_KEY
COHERE_API_KEY=your_key
TAVILY_API_KEY=your_key
```

### Build the knowledge base

The repo ships with a prebuilt index (`faiss_index/`, `chunks.pkl`). To index your own documents:

```bash
python -m rag.vectorstore.build_index --data path/to/your/documents
```

> The supervisor prompt currently describes the knowledge base as being about space and Mars. Edit `agents/supervisor.py` if you index different content.

### Run

Terminal chat:

```bash
python main.py
```

API + UI:

```bash
uvicorn app.main:app --reload --port 8000     # backend
cd frontend && npm install && npm run dev     # UI on http://localhost:5173
```

## API

| Method | Path              | Description                                   |
| ------ | ----------------- | --------------------------------------------- |
| GET    | `/ai/health`      | Health check                                  |
| POST   | `/ai/chat`        | Full answer as JSON                           |
| POST   | `/ai/chat/stream` | SSE stream: `start`, `tool_start`, `tool_end`, `token`, `done`, `error` |

Request body: `{"question": "...", "history": [{"role": "user", "content": "..."}]}`

## Known limitations

This is a working prototype, not a hardened service.

- No authentication, rate limiting, or CORS configuration.
- No automated tests or retrieval evaluation yet.
- The index is loaded with pickle deserialization, so only load index files you built yourself.
- The embedding model is a general sentence-similarity model, not a retrieval-tuned one.
- BM25 uses the default whitespace tokenizer, which is weak for Arabic.
- Adding documents requires rebuilding the index.

## License

See [LICENSE](LICENSE).

