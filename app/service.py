import json

from agents.graph import build_graph


_graph = None


LABELS = {
    "rag": "Knowledge base (RAG)",
    "research": "Web research",
    "analysis": "Analysis",
}


def init_graph():
    global _graph
    _graph = build_graph()


def build_request(question: str, history: list[dict]) -> str:
    """
    Build the request sent to the LangGraph.
    Includes the last 6 conversation messages.
    """
    if not history:
        return question

    convo = "\n".join(
        f"{h['role']}: {h['content']}"
        for h in history[-6:]
    )

    return (
        f"Conversation so far:\n{convo}\n\n"
        f"Current question: {question}"
    )


def _ensure_graph():
    """
    Make sure the graph is initialized before running.
    """
    global _graph

    if _graph is None:
        init_graph()


def _text(content) -> str:
    """
    Normalize chunk.content to plain text.
    Groq/OpenAI return a str, Gemini returns a list of content blocks
    like [{"type": "text", "text": "..."}].
    """
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, str):
                parts.append(p)
            elif isinstance(p, dict) and p.get("type") in (None, "text"):
                parts.append(p.get("text", ""))
        return "".join(parts)

    return ""


def run_chat(
    question: str,
    history: list[dict],
) -> dict:
    """
    Run the graph normally and return the final answer.
    """

    _ensure_graph()

    user_request = build_request(question, history)

    output = _graph.invoke(
        {
            "user_request": user_request,
            "steps": 0,
            "trace": [],
        }
    )

    return {
        "answer": _text(output.get("result", "")),
        "sources": output.get("sources", []),
    }


def _sse(event: str, data: dict) -> str:
    """
    Build a Server-Sent Events message.
    """
    return (
        f"event: {event}\n"
        f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
    )


def stream_chat(
    question: str,
    history: list[dict],
):
    """
    Stream graph execution using SSE.
    """

    _ensure_graph()

    inputs = {
        "user_request": build_request(question, history),
        "steps": 0,
        "trace": [],
    }

    trace = []
    sources = []
    streamed_any = False   # هل وصلت توكنز فعلًا للفرونت؟
    final_answer = ""      # الإجابة الكاملة من node الـ final (fallback)

    try:
        # Tell frontend that execution started
        yield _sse("start", {})

        for mode, data in _graph.stream(
            inputs,
            stream_mode=["updates", "messages"],
        ):

            # ==========================================
            # LLM TOKEN STREAM
            # ==========================================
            if mode == "messages":

                chunk, meta = data

                # Show tokens only from final node
                if meta.get("langgraph_node") == "final":
                    text = _text(chunk.content)

                    if text:
                        streamed_any = True
                        yield _sse("token", {"text": text})

                continue

            # ==========================================
            # NODE UPDATES
            # ==========================================
            if mode == "updates":

                for node, update in data.items():

                    if not update:
                        continue

                    # Add trace information
                    trace.extend(
                        update.get("trace", [])
                    )

                    # Update sources
                    if update.get("sources"):
                        sources = update["sources"]

                    # Keep the final answer as a fallback
                    if node == "final" and update.get("result"):
                        final_answer = _text(update["result"])

                    # ==================================
                    # SUPERVISOR
                    # ==================================
                    if node == "supervisor":

                        for agent in update.get(
                            "next_agent",
                            [],
                        ):

                            if agent in LABELS:
                                yield _sse(
                                    "tool_start",
                                    {
                                        "agent": agent,
                                        "label": LABELS[agent],
                                    },
                                )

                    # ==================================
                    # AGENT FINISHED
                    # ==================================
                    elif node in LABELS:

                        duration_ms = next(
                            (
                                t.get("duration_ms")
                                for t in reversed(trace)
                                if t.get("agent") == node
                            ),
                            None,
                        )

                        yield _sse(
                            "tool_end",
                            {
                                "agent": node,
                                "label": LABELS[node],
                                "duration_ms": duration_ms,
                            },
                        )

        # ==========================================
        # FALLBACK: لو الموديل ما عملش stream
        # ==========================================
        if not streamed_any and final_answer:
            yield _sse("token", {"text": final_answer})

        # ==========================================
        # TOOLS USED
        # ==========================================

        tools_used = [
            LABELS[agent]
            for agent in dict.fromkeys(
                t.get("agent")
                for t in trace
            )
            if agent in LABELS
        ]

        # ==========================================
        # FINISHED
        # ==========================================

        yield _sse(
            "done",
            {
                "sources": sources,
                "tools_used": tools_used,
                "trace": trace,
            },
        )

    except Exception as e:

        yield _sse(
            "error",
            {
                "message": str(e),
            },
        )