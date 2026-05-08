import requests
import numpy as np
import os

from dotenv import load_dotenv

load_dotenv()


class EmbeddingGenerator:

    def __init__(self):

        self.api_key = os.getenv("HF_TOKEN")

        self.url = (
            "https://api-inference.huggingface.co/"
            "pipeline/feature-extraction/"
            "sentence-transformers/all-MiniLM-L6-v2"
        )


    def generate_embeddings(self, texts):

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        embeddings = []

        for text in texts:

            response = requests.post(
                self.url,
                headers=headers,
                json={
                    "inputs": text
                }
            )

            data = response.json()

            if isinstance(data, dict) and "error" in data:

                raise Exception(data["error"])

            embedding = np.mean(
                data,
                axis=0
            )

            embeddings.append(embedding)

        return np.array(
            embeddings,
            dtype="float32"
        )