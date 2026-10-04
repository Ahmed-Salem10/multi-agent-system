import pickle

from rag.embedding.gemini import LocalEmbedding
from rag.vectorstore.faiss_store import VectorStore

from rag.retriever.vectorsearch import vector_search
from rag.retriever.keywordsearch import keyword_search
from rag.retriever.reranker import create_reranker
from rag.retriever.retriever import Retriever

from rag.generation.rag_chain import RAGChain


def create_rag_pipeline():

    # 1. Embeddings (مرة واحدة بس)
    embeddings = LocalEmbedding()

    # 2. Vector Store (محمّل من الديسك)
    vector_store = VectorStore(embeddings)
    vector_store.load("faiss_index")

    # 3. الـ chunks للـ keyword search
    with open("chunks.pkl", "rb") as f:
        documents = pickle.load(f)

    # 4. Retrievers
    vector_retriever = vector_search(vector_store, k=20)
    keyword_retriever = keyword_search(documents, k=20)

    # 5. Reranker
    reranker = create_reranker(top_n=5)

    # 6. Final Retriever
    retriever = Retriever(
        vector_retriever=vector_retriever,
        keyword_retriever=keyword_retriever,
        reranker=reranker,
    )

    # 7. RAG Chain
    return RAGChain(retriever=retriever)