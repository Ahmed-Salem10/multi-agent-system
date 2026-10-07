from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_cohere import CohereRerank

def create_reranker(top_n=5):

    reranker = CohereRerank(model="rerank-v4.0-fast", top_n=5)
    
    return reranker