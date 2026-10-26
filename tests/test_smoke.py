"""Smoke tests: the app starts and the code parses.

These run without Ollama, a Claude API key, or network access, so they work in
CI. ingest.py and query_claude.py do their work at import time (they call
Ollama and Claude), so they are only syntax-checked here, not imported.
"""

import py_compile
from pathlib import Path

from streamlit.testing.v1 import AppTest

SRC = Path(__file__).resolve().parents[1] / "src"
APP = str(SRC / "rag_chat.py")


def test_all_sources_compile():
    for path in SRC.glob("*.py"):
        py_compile.compile(str(path), doraise=True)


def test_dependencies_import():
    # The packages requirements.txt promises, under the names the code uses.
    import anthropic  # noqa: F401
    import chromadb  # noqa: F401
    import pypdf  # noqa: F401
    import streamlit  # noqa: F401
    from langchain_community.document_loaders import PyPDFDirectoryLoader  # noqa: F401
    from langchain_community.vectorstores import Chroma  # noqa: F401
    from langchain_ollama import OllamaEmbeddings  # noqa: F401
    from langchain_text_splitters import RecursiveCharacterTextSplitter  # noqa: F401


def test_chat_app_renders():
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception
    assert any("My Doc Assistant" in m.value for m in at.markdown)
    assert any(t.label == "Claude API Key" for t in at.text_input)


def test_question_without_api_key_asks_for_one():
    at = AppTest.from_file(APP, default_timeout=30).run()
    question = next(t for t in at.text_input if t.label == "Ask a question")
    question.set_value("What does my strategy say about pricing?")
    next(b for b in at.button if b.label == "Send →").click().run()
    assert not at.exception
    assert any("Please enter your Claude API key" in e.value for e in at.error)
