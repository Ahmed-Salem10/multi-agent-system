from langchain_core.prompts import ChatPromptTemplate


RAG_SYSTEM_PROMPT = """
You are a helpful AI assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Do not use information that is not present in the context.
- If the answer cannot be found in the context, say:
  "I don't have enough information in the provided documents."
- Keep the answer clear and concise.
- Do not invent facts.
"""


def create_rag_prompt() -> ChatPromptTemplate:

    return ChatPromptTemplate.from_messages(
        [
            ("system", RAG_SYSTEM_PROMPT),

            (
                "human",
                """
Context:

{context}

Question:

{question}
""",
            ),
        ]
    )