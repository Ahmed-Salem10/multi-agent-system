from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker

def create_reranker(top_n=5):

    model=HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")

    reranker = CrossEncoderReranker(model=model, top_n=top_n)
    
    return reranker