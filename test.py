from agents.graph import build_graph

graph = build_graph()

initial_state = {"user_request": "What does the document say about RAG and characteristics of agentis ai"}

result = graph.invoke(
    initial_state,
    config={"recursion_limit": 15},
)

print(result["result"])