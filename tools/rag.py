from langchain_core.tools import tool
from rag.generation.rag_chain import RAGChain


def create_rag_tool(rag: RAGChain):

    @tool
    def rag_tool(query: str) -> str:
        """Search the uploaded documents and answer using RAG."""
        return rag.invoke(query)

    return rag_tool