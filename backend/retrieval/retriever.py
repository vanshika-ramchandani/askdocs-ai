import numpy as np
from backend.embeddings.embedder import EmbeddingGenerator

class SemanticRetriever:

    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.embedder = EmbeddingGenerator()

    def search(self, query, top_k=5):

        query_embedding = self.embedder.model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.vector_store.index.search(
            query_embedding,
            top_k
        )

        results = []
        seen = set()

        for idx in indices[0]:

            doc = self.vector_store.documents[idx]

            if doc not in seen:

                results.append(doc)
                seen.add(doc)

        return results