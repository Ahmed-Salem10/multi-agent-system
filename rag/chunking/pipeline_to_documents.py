from langchain_core.documents import Document


def convert_to_documents(chunks: list[dict]) -> list[Document]:

    documents = []

    for chunk in chunks:

        documents.append(
            Document(
                page_content=chunk.get("page_content", ""),
                metadata=chunk.get("metadata", {}),
            )
        )

    return documents