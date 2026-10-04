from rag.chunking.chunking_pipeline import ingest_document
from agents.graph import build_graph

if __name__ == "__main__":


    chunks = ingest_document(r"C:\Users\LOQ\Downloads\Agentic_Design_Patterns.pdf")

    graph = build_graph(chunks)

    initial_state = {
        "user_request": "What does the document say about RAG?",
        "next_agent": "",
        "rag_result": "",
        "research_result": "",
        "analysis_result": "",
        "result": "",
        "final_context": "",
    }

    result = graph.invoke(
        initial_state,
        config={"recursion_limit": 15},
    )

    print(result["result"])