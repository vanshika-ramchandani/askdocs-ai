import os
import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()

class EmbeddingGenerator:
    def __init__(self):
        self.api_key = os.getenv("HF_TOKEN")
        # Standard Serverless API endpoint (supports IBM Granite)
        self.model_id = "ibm-granite/granite-embedding-97m-multilingual-r2"
        self.url = f"https://api-inference.huggingface.co/models/{self.model_id}"

    def generate_embeddings(self, texts):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Wait-For-Model": "true"
        }

        embeddings = []

        for text in texts:
            # Direct POST to the model endpoint to bypass the "provider" router
            response = requests.post(
                self.url,
                headers=headers,
                json={"inputs": text},
                timeout=60
            )

            if response.status_code != 200:
                response = requests.post(
                    self.url,
                    headers=headers,
                    json={
                        "inputs": text,
                        "parameters": {"task": "feature-extraction"}
                    }
                )

            data = response.json()
            embedding = np.array(data)

            # Standard mean pooling to get a 1D vector
            if embedding.ndim > 1:
                axis = 1 if embedding.ndim == 3 else 0
                embedding = np.mean(embedding, axis=axis)

            embeddings.append(embedding.flatten())

        return np.array(embeddings, dtype="float32")