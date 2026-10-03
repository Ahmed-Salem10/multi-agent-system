from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


DEFAULT_SEPARATORS = [
    "\n\n",
    "\n",
    " ",
    "",
]


def recursive_document_splitter(
    documents: list[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[Document]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=DEFAULT_SEPARATORS,
        length_function=len,
    )

    chunks = []

    for doc in documents:

        split_texts = splitter.split_text(
            doc.page_content
        )

        for i, text in enumerate(split_texts):

            metadata = doc.metadata.copy()

            metadata["chunk_index"] = i

            chunks.append(
                Document(
                    page_content=text,
                    metadata=metadata,
                )
            )

    return chunks