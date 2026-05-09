# 🚀 Live Demo
https://vanshika-ramchandani-askdocs-ai-frontendapp-ekjrku.streamlit.app/

---

# 🤖 AskDocs AI

AskDocs AI is a production-style Retrieval-Augmented Generation (RAG) application that allows users to chat with documentation websites using AI.

The system crawls documentation pages, generates embeddings, stores them in a FAISS vector database, and provides grounded answers using semantic retrieval and LLMs.

---

# 🚀 Features

- Dynamic documentation crawling
- Recursive link extraction
- Semantic chunking
- Embeddings generation
- FAISS vector database
- Semantic search pipeline
- AI-powered grounded responses
- FastAPI backend
- Streamlit frontend

---

# 🧠 Tech Stack

## Backend
- Python
- FastAPI
- BeautifulSoup
- FAISS
- Sentence Transformers
- Groq API

## Frontend
- Streamlit

## Web Crawling
- Requests
- BeautifulSoup

## AI / RAG
- Semantic Retrieval
- Vector Search
- Embeddings
- LLM Grounding

---

# 📂 Project Structure

```bash
askdocs_ai/
│
├── backend/
│   ├── ingestion/
│   ├── chunking/
│   ├── embeddings/
│   ├── retrieval/
│   ├── rag/
│   ├── llm/
│   └── data/
│
├── frontend/
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/askdocs-ai.git
cd askdocs-ai
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\\Scripts\\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_hugging_face_token_here
```

---

# ▶️ Run Backend

```bash
uvicorn backend.main:app --reload --port 8002
```

---

# ▶️ Run Frontend

```bash
streamlit run frontend/app.py
```

---

# 🌐 Supported Documentation Sites

- React Docs
- FastAPI Docs
- Python Docs
- Tailwind Docs

---

# ⚠️ Limitations

- Best suited for static/server-rendered documentation websites
- Dynamic JavaScript-heavy websites may require browser automation tools such as Playwright

---

# 🏆 Future Improvements

- Hybrid Retrieval (BM25 + Vector Search)
- Cross-Encoder Reranking
- Citation-Based Responses
- Streaming Responses
- Browser Automation Crawling
- Conversation Memory

---

#  📸 Screenshots
<img width="1918" height="866" alt="Screenshot 2026-05-09 165120" src="https://github.com/user-attachments/assets/1c21a588-a038-4ab0-b7f6-1c4da58f38c1" />

<img width="1917" height="867" alt="Screenshot 2026-05-09 165149" src="https://github.com/user-attachments/assets/3ea9c2c1-af77-4b7d-bf4b-60007eaebcd4" />

<img width="1911" height="861" alt="Screenshot 2026-05-09 165142" src="https://github.com/user-attachments/assets/11c8f034-faa1-4856-b4ad-de0aac309852" />


---

# 👨‍💻 Author

Built by Vanshika Ramchandani
