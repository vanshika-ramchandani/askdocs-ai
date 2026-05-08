from backend.retrieval.retriever import SemanticRetriever
from backend.embeddings.vector_store import FAISSVectorStore
from backend.llm.grok_service import GroqService


class RAGPipeline:

    def __init__(self):

        self.vector_store = FAISSVectorStore()

        self.vector_store.load()

        self.retriever = SemanticRetriever(
            self.vector_store
        )

        self.llm = GroqService()

    def ask(self, query):

        retrieved_docs = self.retriever.search(
            query,
            top_k=3
        )

        context = "\n\n".join(retrieved_docs)

        answer = self.llm.generate_response(
            query=query,
            context=context
        )

        return {
            "query": query,
            "answer": answer,
            "retrieved_docs": retrieved_docs
        }