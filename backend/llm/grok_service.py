from groq import Groq
import os

from dotenv import load_dotenv

load_dotenv()


class GroqService:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = "llama-3.1-8b-instant"

    def generate_response(self, query, context):

        prompt = f"""
You are an AI Documentation Assistant.

Answer the user's question using ONLY
the provided documentation context.

Rules:
- Keep answers concise and technical
- Avoid repeating information
- Use bullet points when helpful
- Include code examples only if relevant
- Do not hallucinate
- If answer is unavailable, say so clearly

DOCUMENTATION:
{context}

QUESTION:
{query}

Provide:
1. Short explanation
2. Important technical details
3. Small code example if needed
"""

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return (
            completion
            .choices[0]
            .message.content
        )