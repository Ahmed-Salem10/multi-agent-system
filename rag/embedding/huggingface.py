from sentence_transformers import SentenceTransformer
from rag.embedding.base import BaseEmbedding

class HuggingFaceEmbedding(BaseEmbedding):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_document(self, document: str) -> list[list[float]]:
        """Embed a document into a vector representation."""
        return self.model.encode([document],normalize_embeddings=True).tolist()

    def embed_query(self, query: str) -> list[float]:
        """Embed a query into a vector representation."""
        return self.model.encode([query], normalize_embeddings=True).tolist()