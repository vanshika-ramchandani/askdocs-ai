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

        payload = {
            "model": "jina-embeddings-v2-base-en",
            "input": texts
        }

        response = requests.post(
            self.url,
            headers=headers,
            json=payload
        )

        print("STATUS CODE:", response.status_code)

        print("RAW RESPONSE:")
        print(response.text)

        data = response.json()

        if "data" not in data:

            raise Exception(
                f"Embedding API Error: {data}"
            )

        embeddings = [
            item["embedding"]
            for item in data["data"]
        ]

        return np.array(
            embeddings,
            dtype="float32"
        )