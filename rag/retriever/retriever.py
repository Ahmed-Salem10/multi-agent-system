from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from rag.retriever.vectorsearch import vector_search
from rag.retriever.reranker import create_reranker
from rag.retriever.keywordsearch import keyword_search
from rag.retriever.hybridsearch import hybrid_search

class Retriever:
    def __init__(self, vector_retriever, keyword_retriever, reranker=None):
        self.vector_retriever = vector_retriever
        self.keyword_retriever = keyword_retriever
        self.hybrid_retriever = hybrid_search(vector_retriever, keyword_retriever)
        self.reranker = reranker
        if reranker is not None:
            self.retriever=ContextualCompressionRetriever(base_retriever=self.hybrid_retriever,base_compressor=self.reranker)
        else:
            self.retriever=self.hybrid_retriever

    def retrieve(self, query, k=5):
        """Retrieve documents based on the query using the hybrid retriever."""
        results = self.retriever.invoke(query)[:k]
        return results