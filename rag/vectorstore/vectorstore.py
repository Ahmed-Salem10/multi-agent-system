from langchain_community.vectorstores import FAISS

class VectorStore:
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.db = None  # Placeholder for the actual vector store database

    def create(self,documents):
        """Create a vector store from the provided documents."""
        self.db=FAISS.from_documents(documents, self.embeddings)

    def add_documents(self, documents):
        self.dbf.db.add_documents(documents)

    def search(self,query,k=5):
        self.db.similarity_search(query,k=k)    

    def delete(self,document_id):
        self.db.delete(document_id)

    def save(self, path):
        """Save the vector store to the specified path."""
        self.db.save_local(path)

    def load(self, path):
        """Load the vector store from the specified path."""
        self.db = FAISS.load_local(path, self.embeddings)




