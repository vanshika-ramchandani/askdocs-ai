from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def generate_embeddings(self, chunks):

        embeddings = self.model.encode(chunks)

        return embeddings