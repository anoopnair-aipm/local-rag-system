from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
import anthropic

# Load your local vector database
embedding = OllamaEmbeddings(model="llama3")
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embedding)

# Your question
question = "What are the key points in my product strategy doc?"

# Retrieve the 3 most relevant chunks from your docs
docs = vectorstore.similarity_search(question, k=3)
context = "\n\n".join([doc.page_content for doc in docs])

# Send context + question to Claude
client = anthropic.Anthropic(api_key="YOUR_API_KEY_HERE")

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": f"""Answer the question using ONLY the documents provided below.
If the answer is not in the documents, say 'I could not find this in your documents.'

Documents:
{context}

Question: {question}"""
        }
    ]
)

print(message.content[0].text)
