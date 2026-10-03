import hashlib
import time

from langchain_core.documents import Document


def compute_text_hash(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def enrich_metadata(
    documents: list[Document],
    extra: dict | None = None,
) -> list[Document]:

    extra = extra or {}

    enriched = []

    for doc in documents:

        text = doc.page_content

        metadata = {
            **doc.metadata,
            **extra,
        }

        metadata["doc_id"] = compute_text_hash(text)
        metadata["word_count"] = len(text.split())
        metadata["char_count"] = len(text)
        metadata["ingested_at"] = int(time.time())

        enriched.append(
            Document(
                page_content=text,
                metadata=metadata,
            )
        )

    return enriched