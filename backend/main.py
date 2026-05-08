from fastapi import FastAPI
from pydantic import BaseModel

from backend.rag.rag_pipeline import RAGPipeline
from backend.ingestion.crawler import DocumentationCrawler
from backend.ingestion.parser import DocumentationParser

from backend.chunking.chunker import DocumentChunker
from backend.embeddings.embedder import EmbeddingGenerator
from backend.embeddings.vector_store import FAISSVectorStore

import os
import shutil


app = FastAPI()


class QueryRequest(BaseModel):
    query: str


class URLRequest(BaseModel):
    url: str


rag_pipeline = None


@app.get("/")
def home():

    return {
        "message": "AskDocs AI Running"
    }


@app.post("/process-docs")
def process_docs(request: URLRequest):

    global rag_pipeline

    try:

        BASE_URL = request.url

        # Clear previous data
        if os.path.exists("backend/data/raw_docs"):
            shutil.rmtree("backend/data/raw_docs")

        if os.path.exists("backend/data/vectorstore"):
            shutil.rmtree("backend/data/vectorstore")

        os.makedirs("backend/data/raw_docs", exist_ok=True)

        crawler = DocumentationCrawler(BASE_URL)
        parser = DocumentationParser()

        links = crawler.get_all_links()

        links = links[:25]

        for link in links:

            data = parser.extract_content(link)

            if data:

                filename = (
                    data["title"]
                    .replace("/", "_")
                    .replace(" ", "_")
                    .replace(":", "_")
                )

                parser.save_json(data, filename)

        chunker = DocumentChunker()
        embedder = EmbeddingGenerator()
        vector_store = FAISSVectorStore()

        all_chunks = []

        DATA_DIR = "backend/data/raw_docs"

        for file in os.listdir(DATA_DIR):

            if file.endswith(".json"):

                file_path = os.path.join(DATA_DIR, file)

                with open(file_path, "r", encoding="utf-8") as f:

                    import json

                    data = json.load(f)

                formatted_text = chunker.format_document(data)

                chunks = chunker.create_chunks(
                    formatted_text,
                    chunk_size=800
                )

                all_chunks.extend(chunks)

        embeddings = embedder.generate_embeddings(all_chunks)

        vector_store.add_documents(
            all_chunks,
            embeddings
        )

        vector_store.save()

        rag_pipeline = RAGPipeline()

        return {
            "status": "success",
            "message": "Documentation processed successfully",
            "pages_crawled": len(links),
            "chunks_created": len(all_chunks)
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/ask")
def ask_question(request: QueryRequest):

    global rag_pipeline

    if rag_pipeline is None:

        return {
            "error": "Please process documentation first"
        }

    try:

        result = rag_pipeline.ask(request.query)

        return result

    except Exception as e:

        return {
            "error": str(e)
        }

