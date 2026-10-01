from langchain_classic.retrievers import EnsembleRetriever


def hybrid_search(vector_retriever,keyword_retriever):
    """Combine vector and keyword search using an ensemble retriever."""


    ensemble_retriever = EnsembleRetriever(retrievers=[vector_retriever, keyword_retriever],
                                           weights=[0.5, 0.5]
                                            )
    
    return ensemble_retriever