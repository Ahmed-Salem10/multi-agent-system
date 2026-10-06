from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas import ChatRequest, ChatResponse
from app.service import init_graph, run_chat
from app.service import stream_chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_graph()  # الـRAG والـgraph يتبنوا مرة واحدة وقت التشغيل
    yield

app = FastAPI(title="AI Service", lifespan=lifespan)

@app.get("/ai/health")
def health():
    return {"status": "ok"}

@app.post("/ai/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        result = run_chat(req.question, [h.model_dump() for h in req.history])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {e}")
    return result


@app.post("/ai/chat/stream")
def chat_stream(req: ChatRequest):
    gen = stream_chat(req.question, [h.model_dump() for h in req.history])
    return StreamingResponse(
        gen,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )