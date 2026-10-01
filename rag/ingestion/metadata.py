import hashlib
import time


def compute_text_hash(text: str) -> str:
    """Create a stable SHA-256 hash from the text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def enrich_metadata(
    documents: list[dict],
    extra: dict | None = None
) -> list[dict]:

    extra = extra or {}
    enriched = []

    for doc in documents:
        text = doc.get("text", "")

        metadata = {
            **doc.get("metadata", {}),
            **extra
        }

        metadata["content_hash"] = compute_text_hash(text)
        metadata["word_count"] = len(text.split())
        metadata["char_count"] = len(text)
        metadata["ingested_at"] = int(time.time())

        enriched.append({
            "text": text,
            "metadata": metadata
        })

    return enriched