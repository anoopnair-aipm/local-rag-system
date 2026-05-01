# Local RAG System

> A privacy-first, cost-free alternative to cloud AI for product managers. Ground your LLM in your own documents to eliminate hallucination.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## The Problem

Most PMs use AI like a search engine. Ask a question, get a confident answer — often fabricated.

**Why?** Because the model has never read your actual documents. It's using training data to guess.

- Your proprietary PRDs, strategy docs, and research notes? Never touched.
- Your IP? Sent to cloud APIs.
- Your confidence in AI answers? Zero.

---

## The Solution

**A local RAG system** that forces the AI to read your documents first, then answer.

Instead of:

Question > AI Guesswork > Hallucination

Now:

Question → Retrieve your docs → AI reads them → Answer grounded in reality

### What You Get

✅ **Zero hallucination** — AI reads your docs before answering  
✅ **Privacy** — Your documents never leave your Mac  
✅ **Zero cost** — Runs entirely on your hardware (no API subscriptions)  
✅ **Full chat interface** — No Terminal editing needed  
✅ **Drag & drop uploads** — PDF, Word docs, and text files supported  

---

## How It Works

### 1. Indexing
Your documents are split into 500-word chunks and converted into embeddings (numerical vectors) stored in **ChromaDB** — a local vector database.

### 2. Retrieval
When you ask a question, ChromaDB finds the 3 most relevant chunks from your documents using similarity search.

### 3. Generation
Those chunks are passed to **Claude API** as context. Claude generates an answer grounded in your documents, not its training data.

### 4. Result
**No hallucination. No cloud data loss. Your knowledge, surfaced instantly.**

---

## Tech Stack

| Component | Technology | Why |
|-----------|------------|-----|
| **Local LLM** | [Ollama](https://ollama.com) + LLaMA 3 | Runs on your Mac, no cloud |
| **Vector DB** | [ChromaDB](https://www.trychroma.com/) | Local embeddings storage |
| **Orchestration** | [LangChain](https://www.langchain.com/) | Connects LLM to docs |
| **Chat Interface** | [Streamlit](https://streamlit.io/) | No frontend coding needed |
| **Answer Generation** | [Claude API](https://anthropic.com) | Optional; can use local LLM |

---

## Quick Start

### Prerequisites

- **Mac** with Python 3.10+
- **Ollama** installed (download [here](https://ollama.com))
- **Claude API key** (optional; [get one here](https://console.anthropic.com))

### Installation

```bash
# Clone the repo
git clone https://github.com/anoopnair-aipm/local-rag-system.git
cd local-rag-system

# Create virtual environment
python3 -m venv rag-env
source rag-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download the local LLM
ollama pull llama3
```

### Running the App

```bash
# Start the chat interface
streamlit run src/rag_chat.py
```

Your browser opens automatically. 

**That's it.** No Terminal commands ever again.

---

## Usage

### 1. Add Your Documents

In the sidebar:
- **Drag & drop** PDFs, Word docs, or text files
- Click **Index Now**
- Wait for the ✅ confirmation

### 2. Ask Questions

Type your question in the chat box:

"What are the key points in my product strategy?"
"What does our pricing model say about enterprise customers?"
"Summarize the competitive analysis from my research."

### 3. Get Grounded Answers

Claude reads your documents first, then answers. Only your documents matter — not its training data.

---

## Project Structure

local-rag-system/
├── src/
│   ├── ingest.py              # Load, chunk, embed documents
│   ├── query_claude.py        # Query via Claude API (CLI)
│   └── rag_chat.py            # Web chat interface (Streamlit)
├── docs/
│   └── SETUP.md               # Detailed setup guide
├── my_docs/                   # Your documents go here
├── README.md
├── requirements.txt
└── .gitignore

---

## Why This Matters (For PMs)

This project demonstrates:

| Signal | What it shows |
|--------|---------------|
| **Technical execution** | Not just talk — you shipped end-to-end |
| **PM thinking** | You identified a real problem (hallucination) and built a solution |
| **Full-stack mindset** | Backend logic (RAG) + Frontend UX (Streamlit) both matter |
| **Hands-on leadership** | You can code, architecture, and design all in one project |

**For hiring managers:** This shows you understand AI, can execute, and think beyond product specs.

---

## Limitations

- **Speed:** Local LLM inference is slower than GPT-4 (10–30 seconds per query on M1/M2/M3 Macs)
- **Quality:** LLaMA 3 is excellent for PM tasks, but not enterprise-grade
- **Setup:** Requires basic Terminal comfort (one-time, 15 minutes)
- **Hardware:** Optimized for Apple Silicon (M1/M2/M3); Intel Macs work but slower

---

## Roadmap

- [ ] Google Drive integration for automatic document sync
- [ ] Real-time collaborative indexing
- [ ] Mobile app with same functionality
- [ ] Deploy as public Streamlit Cloud app
- [ ] Support for Notion, Confluence integration
- [ ] Cost analysis dashboard

---

## Example: Real Workflow

**You:** "What was our pricing decision from Q3?"

**Behind the scenes:**
1. ChromaDB searches your docs for pricing-related chunks
2. Finds relevant sections from your Q3 strategy and pricing docs
3. Passes them to Claude with the question
4. Claude reads them and answers based on what's actually there

**Result:** Instant, grounded answer. No hallucination.

---

## Contributing

Found a bug? Want to add a feature? Open an issue or submit a PR.

---

## License

MIT — Free to use and modify for personal and commercial projects.

---

## Questions?

Open an issue on [GitHub](https://github.com/anoopnair-aipm/local-rag-system/issues) or reach out on [LinkedIn](https://linkedin.com/in/anoopnair).

---

**Built to answer:** How do product managers reduce AI hallucination and stay competitive?

*Last updated: May 2026*
