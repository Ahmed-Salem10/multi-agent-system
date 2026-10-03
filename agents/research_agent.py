from agents.supervisor import State
from tools.research import research_tool


def research_agent(state: State):

    user_request = state["user_request"]

    result = research_tool.invoke({
        "query": user_request
    })

    return {
        "research_result": result
    }