from langchain_community.vectorstores import FAISS


class VectorStore:

    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.db = None

    def create(self, documents):
        """Create a FAISS vector store from documents."""

        self.db = FAISS.from_documents(
            documents,
            self.embeddings,
        )

    def add_documents(self, documents):
        """Add documents to the existing vector store."""

        if self.db is None:
            raise ValueError("Vector store has not been created yet.")

        self.db.add_documents(documents)

    def search(self, query, k=5):
        """Search for similar documents."""

        if self.db is None:
            raise ValueError("Vector store has not been created yet.")

        return self.db.similarity_search(
            query,
            k=k,
        )

    def as_retriever(self, k=20):
        """Return a LangChain retriever."""

        if self.db is None:
            raise ValueError("Vector store has not been created yet.")

        return self.db.as_retriever(
            search_kwargs={"k": k}
        )

    def save(self, path):
        """Save the vector store locally."""

        if self.db is None:
            raise ValueError("Vector store has not been created yet.")

        self.db.save_local(path)

    def load(self, path):
        """Load the vector store from disk."""

        self.db = FAISS.load_local(
            path,
            self.embeddings,
            allow_dangerous_deserialization=True,
        )