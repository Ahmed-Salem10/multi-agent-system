from langchain_groq import ChatGroq

from agents.supervisor import State


llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
)


def final_agent(state: State):

    user_request = state["user_request"]

    rag_result = state["rag"]
    research_result = state["research_result"]
    analysis = state["analysis"]

    final_context = f"""
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