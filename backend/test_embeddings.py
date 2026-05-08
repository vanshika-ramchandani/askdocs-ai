import os
import json

from chunking.chunker import DocumentChunker
from embeddings.embedder import EmbeddingGenerator
from embeddings.vector_store import FAISSVectorStore
from retrieval.retriever import SemanticRetriever


# Initialize components
chunker = DocumentChunker()
embedder = EmbeddingGenerator()
vector_store = FAISSVectorStore()

all_chunks = []

DATA_DIR = "backend/data/raw_docs"

# Load all JSON docs
for file in os.listdir(DATA_DIR):

    if file.endswith(".json"):

        file_path = os.path.join(DATA_DIR, file)

        with open(file_path, "r", encoding="utf-8") as f:

            data = json.load(f)

        # Format document
        formatted_text = chunker.format_document(data)

        # Create chunks
        chunks = chunker.create_chunks(formatted_text)

        all_chunks.extend(chunks)

print(f"\nCreated {len(all_chunks)} chunks\n")


# Generate embeddings
embeddings = embedder.generate_embeddings(all_chunks)

print("Embeddings generated successfully\n")


# Add to vector DB
vector_store.add_documents(all_chunks, embeddings)

# Save vector DB
vector_store.save()

print("FAISS vector database saved successfully\n")


# Create retriever
retriever = SemanticRetriever(vector_store)
