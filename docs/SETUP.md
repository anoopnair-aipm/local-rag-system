# Detailed Setup Guide

A step-by-step walkthrough for setting up Local RAG System on your Mac.

## Prerequisites Check

Before you start, verify:

```bash
python3 --version  # Should be 3.10 or higher
```

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/anoopnair-aipm/local-rag-system.git
cd local-rag-system
```

### 2. Install Ollama

Download from [ollama.com](https://ollama.com) and install the Mac app.

Verify:
```bash
ollama --version
```

Pull the LLaMA 3 model:
```bash
ollama pull llama3
```

### 3. Set Up Python Environment

```bash
python3 -m venv rag-env
source rag-env/bin/activate
```

You should see `(rag-env)` at the start of your Terminal prompt.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Get Your Claude API Key (Optional)

If using Claude for answer generation (recommended):

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Click **API Keys**
3. Create a new key
4. Copy it

You'll paste this in the Streamlit sidebar when you launch the app.

---

## Running the App

```bash
streamlit run src/rag_chat.py
```

Your browser opens to `http://localhost:8501`

---

## Troubleshooting

### Error: `ModuleNotFoundError`

**Fix:**
```bash
pip install -r requirements.txt
```

### Error: `Ollama connection error`

**Fix:** Make sure Ollama is running. Open the Ollama app from Applications.

### Error: `No documents indexed`

**Fix:** Drag PDFs into the sidebar and click "Index Now"

---

## Common Questions

**Q: Do my documents get sent to the cloud?**  
A: No. ChromaDB stays on your Mac. Only document chunks are sent to Claude API (if you use Claude).

**Q: Can I use local LLM only?**  
A: Yes. Edit `src/rag_chat.py` to use `OllamaLLM` instead of Claude API.

**Q: How do I add more documents?**  
A: Use the sidebar uploader. No Terminal needed.

**Q: Is this production-ready?**  
A: It's built for personal PM productivity. For production, add error handling, logging, and authentication.

---

## Next Steps

- Start with 1–2 sample PDFs to test the workflow
- Add your actual PRDs and strategy docs once you're comfortable
- Customize chunk size in `src/ingest.py` if needed (default: 500 words)
