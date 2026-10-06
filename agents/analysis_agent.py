from langchain_groq import ChatGroq

from agents.supervisor import State


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,reasoning_effort="low",max_tokens=1000
)


def analysis_agent(state: State):

    user_request = state["user_request"]
    rag_result = state.get("rag_result", "")
    research_result = state.get("research_result", "")

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
        "analysis_result": response.content
    }