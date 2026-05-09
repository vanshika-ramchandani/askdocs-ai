import os
import time
import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()

class EmbeddingGenerator:
    def __init__(self):
        self.api_key = os.getenv("HF_TOKEN")
        self.model_id = "intfloat/multilingual-e5-large"
        self.url = f"https://router.huggingface.co/hf-inference/models/{self.model_id}/pipeline/feature-extraction"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _embed_one(self, text, retries=3):
        for attempt in range(retries):
            try:
                response = requests.post(
                    self.url,
                    headers=self.headers,
                    json={"inputs": text, "options": {"wait_for_model": True}},
                    timeout=60
                )

                if response.status_code == 503:
                    print(f"Model loading, waiting 20s...")
                    time.sleep(20)
                    continue

                if response.status_code == 429:
                    wait = 30 * (attempt + 1)
                    print(f"Rate limited, waiting {wait}s...")
                    time.sleep(wait)
                    continue

                if not response.ok:
                    raise RuntimeError(f"HF API error {response.status_code}: {response.text[:300]}")

                data = response.json()
                embedding = np.array(data, dtype="float32")

                if embedding.ndim == 3:
                    embedding = np.mean(embedding, axis=1)
                if embedding.ndim == 2:
                    embedding = np.mean(embedding, axis=0)

                return embedding.flatten()

            except RuntimeError:
                raise
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(5)
                else:
                    raise

    def generate_embeddings(self, texts):
        embeddings = []
        for i, text in enumerate(texts):
            embedding = self._embed_one(text)
            embeddings.append(embedding)
            print(f"Embedded chunk {i+1}/{len(texts)}")
            time.sleep(0.5)  # be gentle with free tier

        return np.array(embeddings, dtype="float32")