
def vector_search(vector_store, k=20):
    """Create a vector retriever from the FAISS vector store."""

    return vector_store.as_retriever(k=k)