from pathlib import Path

from rag.ingestion.loader.pdf_loader import pdf_loader
from rag.ingestion.cleaner import clean_documents
from rag.ingestion.metadata import enrich_metadata
from rag.chunking.recursive_chunking import recursive_document_splitter
from langchain_core.documents import Document


def ingest_document(file_path: str) -> list[Document]:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # 1. Load
    documents = pdf_loader(str(path))

    # 2. Clean
    documents = clean_documents(documents)

    # 3. Metadata
    documents = enrich_metadata(
        documents,
        extra={
            "source": path.name,
        },
    )

    # 4. Chunk
    chunks = recursive_document_splitter(
        documents,
        chunk_size=1000,
        chunk_overlap=150,
    )

    return chunks