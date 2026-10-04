from rag.embedding.gemini import LocalEmbedding
from rag.vectorstore.faiss_store import VectorStore

from rag.retriever.vectorsearch import vector_search
from rag.retriever.keywordsearch import keyword_search
from rag.retriever.reranker import create_reranker
from rag.retriever.retriever import Retriever

from rag.generation.rag_chain import RAGChain


def create_rag_pipeline(documents):

    # 1. Embeddings
    embeddings = LocalEmbedding()

    # 2. Vector Store
    vector_store = VectorStore(embeddings)
    vector_store.create(documents)

    # 3. Vector Retriever
    vector_retriever = vector_search(
        vector_store,
        k=20,
    )

    # 4. Keyword Retriever
    keyword_retriever = keyword_search(
        documents,
        k=20,
    )

    # 5. Reranker
    reranker = create_reranker(
        top_n=5,
    )

    # 6. Final Retriever
    retriever = Retriever(
        vector_retriever=vector_retriever,
        keyword_retriever=keyword_retriever,
        reranker=reranker,
    )

    # 7. RAG Chain
    rag = RAGChain(
        retriever=retriever,
    )

    return rag