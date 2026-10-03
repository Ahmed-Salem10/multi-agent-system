from langchain_groq import ChatGroq

from agents.supervisor import State


llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
)


def analysis_agent(state: State):

    user_request = state["user_request"]
    rag_result = state["rag"]
    research_result = state["research_result"]

    response = llm.invoke(
        f"""
You are an analysis agent.

Analyze the information collected by the other agents.

User request:
{user_request}

Information from RAG:
{rag_result}

Information from web research:
{research_result}

Tasks:
- Compare the available information.
- Identify the relevant information.
- Remove irrelevant information.
- Do not invent facts.
- Prepare a clear analysis for the final agent.
"""
    )

    return {
        "analysis": response.content
    }