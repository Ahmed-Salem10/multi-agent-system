import re


def clean_text(text: str) -> str:
    """Clean extracted text before chunking."""

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove control characters
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Remove spaces at the beginning/end of each line
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Put the cleaned lines back together
    text = "\n".join(lines)

    # Remove repeated spaces
    text = re.sub(r" {2,}", " ", text)

    # Limit excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_documents(documents: list[dict]) -> list[dict]:
    """Clean all documents and remove empty ones."""

    cleaned = []

    for doc in documents:
        text = clean_text(doc.get("text", ""))

        if text:
            cleaned.append({
                "text": text,
                "metadata": doc.get("metadata", {})
            })

    return cleaned