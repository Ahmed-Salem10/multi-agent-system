from sentence_transformers import SentenceTransformer

from .base import BaseEmbedding


class LocalEmbedding(BaseEmbedding):

    def __init__(
        self,
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    ):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        return self.model.encode(
            documents,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True,
        ).tolist()

    def embed_query(self, query: str) -> list[float]:
        return self.model.encode(
            query,
            normalize_embeddings=True,
        ).tolist()