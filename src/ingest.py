from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# Load all PDFs from your folder
loader = PyPDFDirectoryLoader("my_docs/")
docs = loader.load()
print(f"Loaded {len(docs)} document(s).")

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"Split into {len(chunks)} chunks.")

# Embed and store locally
embedding = OllamaEmbeddings(model="llama3")
vectorstore = Chroma.from_documents(chunks, embedding, persist_directory="chroma_db")
print("✅ Documents indexed successfully.")
