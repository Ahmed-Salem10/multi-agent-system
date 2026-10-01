from langchain_core.documents import Document


def build_context(documents: list[Document]) -> str:
    """
    Convert retrieved documents into a single context string.
    """

    if not documents:
        return ""

    context_parts = []

    for i, document in enumerate(documents, start=1):

        content = document.page_content
        metadata = document.metadata

        source = metadata.get("source", "Unknown")
        page = metadata.get("page", "Unknown")

        context_parts.append(
            f"[Source {i}]\n"
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content:\n{content}"
        )

    return "\n\n".join(context_parts)