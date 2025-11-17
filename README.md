
# ⚡ Smart RAG Engine with Auto-Reindex  
A self-improving Retrieval-Augmented Generation engine designed for startup-level GenAI products.

![Startup Ready](https://img.shields.io/badge/Startup-Ready-orange)
![RAG](https://img.shields.io/badge/Technique-RAG-blue)
![Self Improving](https://img.shields.io/badge/Feature-Self--Improving-brightgreen)

This RAG system:
- Retrieves top-k chunks  
- Generates an LLM answer  
- Detects low-quality responses  
- Automatically re-chunks and re-indexes documents  

Perfect for knowledge bases, internal tools, and intelligent document systems.

---

## ⭐ Features
- Self-repairing retrieval  
- Chroma vector DB  
- Clean architecture  
- Easy to extend  
- Developer-friendly design  

---

## 📁 Folder Structure
```
rag-autoreindex/
│   ingest.py
│   indexer.py
│   retriever.py
│   qa.py
│   utils.py
│   requirements.txt
│   README.md
│
└── data/docs/
    └── (your .txt / .md files)
```

---

## ⚡ Quickstart

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add documents  
Place `.txt` or `.md` files in:
```
data/docs/
```

### 3. Set OpenAI key  
Create `.env`:
```
OPENAI_API_KEY=sk-xxxx
```

### 4. Ingest documents
```bash
python ingest.py
```

### 5. Run Q&A engine
```bash
python qa.py
```

---

## 🧠 Auto-Reindex Flow
```
Query → Retrieve → Answer
       ↓
Is answer low-quality?
     Yes → Rechunk → Reindex → Improved retrieval
```

---

## 🌱 Extend This Project
- Add hybrid search  
- Persist Chroma with DuckDB  
- Add FastAPI server  
- Track quality metrics  

---

## 📜 License  
MIT License
