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
- Multi-documentation support

---

# 🧠 Tech Stack

## Backend
- Python
- FastAPI
- FAISS
- Sentence Transformers
- Groq API

## Frontend
- Streamlit

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
GROQ_API_KEY=your_api_key_here
```

---

# ▶️ Run Backend

```bash
uvicorn backend.main:app --reload --port 8001
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

# 👨‍💻 Author

Built by Vanshika Ramchandani