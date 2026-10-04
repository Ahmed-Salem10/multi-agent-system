from pathlib import Path
from rag.chunking.chunking_pipeline import ingest_document
from rag.embedding.gemini import LocalEmbedding
from rag.vectorstore.faiss_store import VectorStore

DATA_PATH = Path(r"C:\Users\LOQ\Downloads\NASA")

if DATA_PATH.is_dir():
    files = [
        f for f in DATA_PATH.iterdir()
        if f.suffix.lower() in {".pdf", ".txt", ".docx", ".md"}
    ]
else:
    files = [DATA_PATH]

chunks = []
for file in files:
    chunks.extend(ingest_document(str(file)))

print(f"Total chunks: {len(chunks)}")

store = VectorStore(LocalEmbedding())
store.create(chunks)
store.save("faiss_index")
import pickle

with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)
print("Index saved.")