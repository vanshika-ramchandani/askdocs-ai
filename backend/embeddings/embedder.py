import requests
import numpy as np
import os

from dotenv import load_dotenv

load_dotenv()


class EmbeddingGenerator:

    def __init__(self):

        self.api_key = os.getenv("JINA_API_KEY")

        self.url = "https://api.jina.ai/v1/embeddings"


    def generate_embeddings(self, texts):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        embeddings = []

        for text in texts:

            payload = {
                "model": "jina-embeddings-v2-base-en",
                "input": [text]
            }

            response = requests.post(
                self.url,
                headers=headers,
                json=payload
            )

            data = response.json()

            embedding = data["data"][0]["embedding"]

            embeddings.append(embedding)

        return np.array(
            embeddings,
            dtype="float32"
        )