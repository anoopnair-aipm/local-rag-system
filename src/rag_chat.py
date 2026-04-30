import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
import anthropic

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="My Doc Assistant",
    page_icon="🧠",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0d0d0d;
    color: #e8e8e8;
}

.stApp {
    background-color: #0d0d0d;
}

/* Header */
.header-block {
    border-left: 3px solid #00ff88;
    padding: 0.4rem 0 0.4rem 1rem;
    margin-bottom: 1.5rem;
}
.header-block h1 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.4rem;
    font-weight: 600;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.5px;
}
.header-block p {
    font-size: 0.78rem;
    color: #888;
    margin: 0.2rem 0 0 0;
    font-family: 'IBM Plex Mono', monospace;
}

/* Chat messages */
.msg-user {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 8px 8px 2px 8px;
    padding: 0.85rem 1rem;
    margin: 0.5rem 0 0.5rem 3rem;
    font-size: 0.9rem;
    color: #e8e8e8;
    line-height: 1.6;
}
.msg-assistant {
    background: #111;
    border: 1px solid #00ff8830;
    border-left: 3px solid #00ff88;
    border-radius: 2px 8px 8px 8px;
    padding: 0.85rem 1rem;
    margin: 0.5rem 3rem 0.5rem 0;
    font-size: 0.9rem;
    color: #d4d4d4;
    line-height: 1.7;
}
.label-user {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #555;
    text-align: right;
    margin: 0.2rem 0 0 0;
    padding-right: 0.2rem;
}
.label-assistant {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #00ff8870;
    margin: 0.2rem 0 0 0;
    padding-left: 0.2rem;
}

/* Source chunks */
.source-block {
    background: #0a0a0a;
    border: 1px dashed #2a2a2a;
    border-radius: 4px;
    padding: 0.5rem 0.75rem;
    margin-top: 0.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #555;
}

/* Status bar */
.status-bar {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #444;
    padding: 0.4rem 0;
    border-top: 1px solid #1a1a1a;
    margin-top: 1rem;
}
.status-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    background: #00ff88;
    border-radius: 50%;
    margin-right: 6px;
    vertical-align: middle;
}

/* Input */
.stTextInput > div > div > input {
    background-color: #111 !important;
    color: #e8e8e8 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 0.9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 0 1px #00ff8840 !important;
}

/* Buttons */
.stButton > button {
    background: transparent !important;
    color: #00ff88 !important;
    border: 1px solid #00ff8850 !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    padding: 0.4rem 1rem !important;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: #00ff8810 !important;
    border-color: #00ff88 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0a0a0a;
    border-right: 1px solid #1a1a1a;
}
section[data-testid="stSidebar"] .stMarkdown {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #666;
}

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    api_key = st.text_input(
        "Claude API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Get your key from console.anthropic.com"
    )
    db_path = st.text_input(
        "ChromaDB Path",
        value="chroma_db",
        help="Path to your local vector database folder"
    )
    num_chunks = st.slider("Chunks to retrieve", min_value=1, max_value=6, value=3,
                           help="How many document sections to retrieve per question")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("**How it works**")
    st.markdown("""
1. Your question →
2. ChromaDB finds relevant chunks →
3. Claude answers from your docs →
4. No hallucination
    """)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-block">
    <h1>🧠 My Doc Assistant</h1>
    <p>local rag · powered by claude · zero hallucination</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Render chat history ───────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="label-user">you</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg-assistant">{msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="label-assistant">∎ assistant · grounded in your docs</div>', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("---")
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Ask a question",
            placeholder="What does my product strategy say about pricing?",
            label_visibility="collapsed"
        )
    with col2:
        submitted = st.form_submit_button("Send →")

# ── Process query ─────────────────────────────────────────────────────────────
if submitted and user_input.strip():
    if not api_key:
        st.error("Please enter your Claude API key in the sidebar.")
    else:
        # Save user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Retrieving from your docs..."):
            try:
                # Load ChromaDB
                embedding = OllamaEmbeddings(model="llama3")
                vectorstore = Chroma(
                    persist_directory=db_path,
                    embedding_function=embedding
                )

                # Retrieve relevant chunks
                docs = vectorstore.similarity_search(user_input, k=num_chunks)
                context = "\n\n".join([doc.page_content for doc in docs])

                if not context.strip():
                    answer = "I could not find relevant information in your documents for this question."
                else:
                    # Call Claude
                    client = anthropic.Anthropic(api_key=api_key)
                    response = client.messages.create(
                        model="claude-opus-4-5",
                        max_tokens=1024,
                        messages=[
                            {
                                "role": "user",
                                "content": f"""You are a precise assistant. Answer the question using ONLY the document excerpts provided below.
If the answer is not found in the documents, respond with: 'I could not find this in your documents.'
Do not make up information. Do not use prior knowledge.

Document excerpts:
{context}

Question: {user_input}"""
                            }
                        ]
                    )
                    answer = response.content[0].text

                # Save and display answer
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)}")

# ── Status bar ────────────────────────────────────────────────────────────────
msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
st.markdown(f"""
<div class="status-bar">
    <span class="status-dot"></span>
    local · chroma_db · {msg_count} question(s) asked this session
</div>
""", unsafe_allow_html=True)

