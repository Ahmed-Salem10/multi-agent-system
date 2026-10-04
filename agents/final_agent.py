from langchain_groq import ChatGroq

from agents.supervisor import State


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)


def final_agent(state: State):

    user_request = state["user_request"]
    rag_result = state.get("rag_result", "")
    research_result = state.get("research_result", "")
    analysis = state.get("analysis_result", "")

    final_context = analysis if analysis else f"""
RAG information:
{rag_result}

Research information:
{research_result}

Analysis:
{analysis}
"""

    response = llm.invoke(
        f"""
You are the final answer agent.

Answer the user's request using the information
provided by the other agents.

User request:
{user_request}

Context:
{final_context}

Rules:
- Answer clearly and directly.
- Use only the provided information.
- Do not invent facts.
- If some information is unavailable, say so.
"""
    )

    return {
        "final_context": final_context,
        "result": response.content
    }