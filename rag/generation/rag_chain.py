from rag.generation.context_builder import build_context
from rag.generation.prompt import create_rag_prompt
from rag.generation.llm import get_llm


class RAGChain:

    def __init__(self, retriever):
        self.retriever = retriever
        self.prompt = create_rag_prompt()
        self.llm = get_llm()

    def invoke(self, question: str) -> str:

        # 1. Retrieve relevant documents
        documents = self.retriever.retrieve(question)

        # 2. Build context
        context = build_context(documents)

        # 3. Create prompt
        messages = self.prompt.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        # 4. Ask LLM
        response = self.llm.invoke(messages)

        citations = []

        for i, document in enumerate(documents, start=1):

            citations.append(
                {
                    "id": i,
                    "source": document.metadata.get(
                        "source",
                        "Unknown"
                    ),
                    "page": document.metadata.get(
                        "page",
                        "Unknown"
                    ),
                    "chunk_index": document.metadata.get(
                        "chunk_index",
                        None
                    ),
                }
            )

        return {"answer":response.content,
                "citation":citations}