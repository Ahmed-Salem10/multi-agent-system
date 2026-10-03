from agents.supervisor import State
from tools.rag import create_rag_tool


def create_rag_agent(rag):
    rag_tool = create_rag_tool(rag)

    def rag_agent(state: State):
        user_request = state["user_request"]

        result = rag_tool.invoke({
            "query": user_request
        })

        return {
            "rag": result
        }

    return rag_agent