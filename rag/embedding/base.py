from abc import ABC, abstractmethod

@abstractmethod
class BaseEmbedding(ABC):
    @abstractmethod
    def embed_document(self, document: str) -> list[list[float]]:
        """Embed a document into a vector representation."""
        pass

    @abstractmethod
    def embed_query(self, query: str) -> list[float]:
        """Embed a query into a vector representation."""
        pass

    