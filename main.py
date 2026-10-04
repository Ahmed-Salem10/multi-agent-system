from agents.graph import build_graph

graph = build_graph()

while True:
    question = input("\nYou: ").strip()
    if question.lower() in ("exit", "quit", "q"):
        break

    started = False
    for mode, data in graph.stream(
        {"user_request": question},
        stream_mode=["updates", "messages"],
    ):
        if mode == "updates":
            for node, output in data.items():
                if node == "supervisor":
                    print(f"🧭 supervisor → {output['next_agent']}")
                elif node != "final":
                    print(f"🔧 tool used: {node}")
        else:
            chunk, meta = data
            if meta["langgraph_node"] == "final" and chunk.content:
                if not started:
                    print("\nAssistant: ", end="")
                    started = True
                print(chunk.content, end="", flush=True)
    print()