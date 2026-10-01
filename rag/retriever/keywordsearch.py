from langchain_community.retrievers import BM25Retriever

def keyword_search(documents, k):

    retriever=BM25Retriever.from_documents(documents)
    retriever.k=k
    return retriever

