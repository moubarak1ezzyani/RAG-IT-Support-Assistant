# RAG-IT-Support-Assistant
A reliable RAG-powered assistant for IT technicians to query procedures, incidents, and FAQs from PDF documentation.

## 📂 File Tree & Naming Convention
```Plaintext
Smart-IT-Support-RAG/
│
├── .env                       # 🔐 API Keys (HF_TOKEN) - GitIgnore this!
├── .gitignore                 # 🙈 File to ignore .env and /chroma_db
├── requirements.txt           # 📦 Dependencies (langchain, chromadb, etc.)
├── README.md                  # 📖 Documentation
│
├── data/                      # 📂 Source Files
│   └── The-IT-Support-Handbook.pdf
│
├── chroma_db/                 # 💾 Vector Database (Generated automatically)
│
└── src/                       # 🧠 Source Code
    ├── __init__.py            # Makes 'src' a package
    ├── config.py              # ⚙️ Central config (Paths, Model Names)
    │
    ├── embedding_client.py    # 🔌 Loads BGE-M3 model (The "Translator")
    ├── ingestion.py           # 🏭 PDF -> Vectors (Run this once)
    ├── vector_store.py        # 🔍 Search Logic (Finds relevant text)
    │
    ├── llm_client.py          # 🤖 Loads Mistral LLM (The "Writer")
    ├── rag_pipeline.py        # 🔗 The Core: Search + LLM generates answer
    │
    └── app.py                 # 🖥️ Main entry point (The Interface)
```

## 🌿 GitHub Branch Strategy (Git Flow)
![alt text](image.png)
``
feat/data-ingestion
feat/vector-db
feat/rag
feat/backend
feat/db-postgres
feat/ml-flow-tracking
feat/ml-flow-registry
feat/ci-cd
feat/deploy