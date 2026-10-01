from typing import Any
from langchain_text_splitters import RecursiveCharacterTextSplitter


DEFAULT_SEPARATORS = ["\n\n", "\n", " ", ""]


def get_text_splitter(
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
    separators: list[str] | None = None,
) -> RecursiveCharacterTextSplitter:

    if separators is None:
        separators = DEFAULT_SEPARATORS

    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
        length_function=len,
        is_separator_regex=False,
    )


def recursive_text_splitter(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
    separators: list[str] | None = None,
) -> list[str]:

    if not text or not text.strip():
        return []

    splitter = get_text_splitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
    )

    return splitter.split_text(text)


def recursive_document_splitter(
    documents: list[dict[str, Any]],
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
    separators: list[str] | None = None,
) -> list[dict[str, Any]]:

    if not documents:
        return []

    splitter = get_text_splitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
    )

    chunk_documents = []

    for doc in documents:

        text = doc.get("text", "")
        metadata = doc.get("metadata", {})

        if not text or not text.strip():
            continue

        chunks = splitter.split_text(text)

        for i, chunk in enumerate(chunks):

            chunk_metadata = metadata.copy()

            chunk_metadata["chunk_index"] = i

            chunk_documents.append({
                "text": chunk,
                "metadata": chunk_metadata,
            })

    return chunk_documents