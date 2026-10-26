# Local RAG System

> A local-first document assistant for product managers. Your documents are indexed on your Mac, and Claude answers from the most relevant excerpts, so answers are grounded in what you've actually written.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## The Problem

Most PMs use AI like a search engine. Ask a question, get a confident answer — often fabricated.

**Why?** Because the model has never read your actual documents. It's using training data to guess.

- Your proprietary PRDs, strategy docs, and research notes? Never touched.
- Your IP? Pasted wholesale into chat windows.
- Your confidence in AI answers? Zero.

---

## The Solution

**A local RAG system** that forces the AI to read your documents first, then answer.

Instead of:

Question > AI Guesswork > Hallucination

Now:

Question → Retrieve your docs → AI reads them → Answer grounded in reality

### What You Get

✅ **Fewer hallucinations** — Claude is told to answer only from your retrieved excerpts, and to say so when they don't cover the question  
✅ **Local index** — Your documents, embeddings, and vector database stay on your Mac; only the few excerpts relevant to each question are sent to the Claude API  
✅ **Low cost** — Embeddings run locally with Ollama for free; you pay only for the Claude API calls that answer questions  
✅ **Chat interface** — Ask questions in a Streamlit app; Terminal is only needed to index documents  
✅ **PDF indexing** — Put PDFs in `my_docs/` and index them with one command  

---

## How It Works

### 1. Indexing
Your PDFs are split into 500-character chunks (with 50 characters of overlap) and converted into embeddings (numerical vectors) locally by **Ollama** (LLaMA 3), then stored in **ChromaDB** — a local vector database.

### 2. Retrieval
When you ask a question, ChromaDB finds the 3 most relevant chunks from your documents using similarity search.

### 3. Generation
Those chunks are sent to the **Claude API** with your question. Claude is instructed to answer only from those excerpts, and to say "I could not find this in your documents" when they don't contain the answer.

### 4. Result
**Answers tied to your own documents. Your full documents and index never leave your Mac.**

---

## Tech Stack

| Component | Technology | Why |
|-----------|------------|-----|
| **Embeddings** | [Ollama](https://ollama.com) + LLaMA 3 | Runs on your Mac, no cloud |
| **Vector DB** | [ChromaDB](https://www.trychroma.com/) | Local embeddings storage |
| **Orchestration** | [LangChain](https://www.langchain.com/) | Connects LLM to docs |
| **Chat Interface** | [Streamlit](https://streamlit.io/) | No frontend coding needed |
| **Answer Generation** | [Claude API](https://anthropic.com) | Required; receives only the retrieved excerpts |

---

## Quick Start

### Prerequisites

- **Mac** with Python 3.10+
- **Ollama** installed (download [here](https://ollama.com))
- **Claude API key** ([get one here](https://console.anthropic.com))

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

# Download the local embedding model
ollama pull llama3
```

### Running the App

```bash
# Index your documents (put your PDFs in my_docs/ first)
python src/ingest.py

# Start the chat interface
streamlit run src/rag_chat.py
```

Your browser opens automatically.

**That's it.** Re-run `python src/ingest.py` only when you add documents.

---

## Usage

### 1. Add Your Documents

- Copy your **PDFs** into the `my_docs/` folder
- Run `python src/ingest.py`
- Wait for the ✅ `Documents indexed successfully.` confirmation

### 2. Ask Questions

Paste your Claude API key in the sidebar, then type your question in the chat box:

"What are the key points in my product strategy?"
"What does our pricing model say about enterprise customers?"
"Summarize the competitive analysis from my research."

### 3. Get Grounded Answers

Claude reads the retrieved excerpts first, then answers from them — and says so when your documents don't cover the question. For decisions that matter, check the answer against the source document.

---

## Project Structure

local-rag-system/
├── src/ 
│   ├── ingest.py              # Load, chunk, embed documents
│   ├── query_claude.py        # Query via Claude API (CLI)
│   └── rag_chat.py            # Web chat interface (Streamlit)
├── docs/
│   └── SETUP.md               # Detailed setup guide
├── my_docs/                   # Your PDFs go here (gitignored)
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

- **Privacy:** The excerpts retrieved for each question are sent to Anthropic's API — don't index documents you can't share with a cloud provider
- **Retrieval quality:** Answers can only be as good as the retrieved excerpts; LLaMA 3 is a general-purpose model, not a dedicated embedding model, so retrieval can miss relevant passages
- **File types:** PDF only for now
- **Speed:** Indexing runs embeddings locally, so large document sets take a while (slower on Intel Macs)
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

**Result:** A fast answer grounded in your own documents.

---

## Contributing

Found a bug? Want to add a feature? Open an issue or submit a PR.

---

## License

MIT — Free to use and modify for personal and commercial projects.

---

## Questions?

Open an issue on [GitHub](https://github.com/anoopnair-aipm/local-rag-system/issues) or reach out on [LinkedIn](https://www.linkedin.com/in/anoopsnair/).

---

**Built to answer:** How do product managers reduce AI hallucination and stay competitive?

*Last updated: October 2026*
