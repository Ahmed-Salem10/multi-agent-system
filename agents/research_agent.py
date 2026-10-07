from agents.supervisor import State
from tools.research import research_tool


def research_agent(state: State):
    user_request = state["user_request"]

    result = research_tool.invoke({
        "query": user_request
    })

    print("\n🔍 RESEARCH RESULT:")
    print(result)
    print()

    return {
        "research_result": result,
        "sources": [
    {
        "title": r.get("title", ""),
        "url": r.get("url", ""),
    }
    for r in result
    ]
    }