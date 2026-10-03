import re
from langchain_core.documents import Document


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    text = re.sub(
        r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]",
        "",
        text,
    )

    text = text.replace("\t", " ")

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    text = "\n".join(lines)

    text = re.sub(r" {2,}", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_documents(documents: list[Document]) -> list[Document]:

    cleaned = []

    for doc in documents:

        text = clean_text(doc.page_content)

        if text:

            cleaned.append(
                Document(
                    page_content=text,
                    metadata=doc.metadata.copy(),
                )
            )

    return cleaned