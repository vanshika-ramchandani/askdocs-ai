import os
import numpy as np
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class EmbeddingGenerator:
    def __init__(self):
        self.api_key = os.getenv("HF_TOKEN")
        # Use the standard API endpoint to avoid deployment routing issues
        self.model_id = "ibm-granite/granite-embedding-97m-multilingual-r2"
        self.url = f"https://api-inference.huggingface.co/models/{self.model_id}"

    def generate_embeddings(self, texts):
        # Deployment environments often need a clear User-Agent
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Wait-For-Model": "true",
            "User-Agent": "MyEmbeddingApp/1.0"
        }

        embeddings = []

        for text in texts:
            # Wrap in a retry loop for deployment stability
            for attempt in range(3):
                try:
                    response = requests.post(
                        self.url,
                        headers=headers,
                        json={"inputs": text},
                        timeout=30
                    )

                    # Check if we got JSON back
                    if response.status_code == 200:
                        data = response.json()
                        embedding = np.array(data)
                        
                        # Mean pooling for sequence-to-vector
                        if embedding.ndim > 1:
                            axis = 1 if embedding.ndim == 3 else 0
                            embedding = np.mean(embedding, axis=axis)
                        
                        embeddings.append(embedding.flatten())
                        break # Success, move to next text
                    
                    elif response.status_code == 503:
                        # Model is loading, wait and retry
                        time.sleep(5)
                        continue
                    else:
                        raise Exception(f"Status {response.status_code}: {response.text}")

                except requests.exceptions.JSONDecodeError:
                    # This captures the "line 1 column 1" error
                    print(f"Deployment Error: API returned non-JSON response. Raw: {response.text[:100]}")
                    time.sleep(2)
                except Exception as e:
                    if attempt == 2: raise e
                    time.sleep(2)

        return np.array(embeddings, dtype="float32")