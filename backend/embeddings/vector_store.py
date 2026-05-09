import faiss
import numpy as np
import pickle
import os

class FAISSVectorStore:

    def __init__(self, dimension=1024):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add_documents(self, chunks, embeddings):

        embeddings = np.array(embeddings).astype("float32")

        self.index.add(embeddings)
        self.documents.extend(chunks)

    def save(self):

        os.makedirs("backend/data/vectorstore", exist_ok=True)

        faiss.write_index(
            self.index,
            "backend/data/vectorstore/faiss.index"
        )

        with open("backend/data/vectorstore/documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)

    def load(self):

        self.index = faiss.read_index(
            "backend/data/vectorstore/faiss.index"
        )

        with open("backend/data/vectorstore/documents.pkl", "rb") as f:
            self.documents = pickle.load(f)