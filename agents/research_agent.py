from agents.supervisor import State
from tools.research import research_tool


def research_agent(state: State):
    user_request = state["user_request"]

    result = research_tool.invoke({"query": user_request})

    if not isinstance(result, list):
        return {
            "research_result": [],
            "sources": [],
        }

    return {
        "research_result": result,
        "sources": [
            {"title": r.get("title", ""), "url": r.get("url", "")}
            for r in result
            if isinstance(r, dict)
        ],
    }
