from abc import abstractmethod
from langchain_core.embeddings import Embeddings


class BaseEmbedding(Embeddings):
    @abstractmethod
    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """Embed a list of documents into vector representations."""
        pass

    @abstractmethod
    def embed_query(self, query: str) -> list[float]:
        """Embed a query into a vector representation."""
        pass

    