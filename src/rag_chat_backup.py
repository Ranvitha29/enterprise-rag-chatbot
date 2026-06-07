print("RAG FILE WORKING")
from sentence_transformers import SentenceTransformer
import chromadb
import ollama

# =====================
# EMBEDDING MODEL
# =====================
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# =====================
# VECTOR DB (PERSISTENT FIX)
# =====================
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("rag_store")

# =====================
# LOAD FILE
# =====================
import os

documents = []

data_folder = "data"

for filename in os.listdir(data_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(data_folder, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

            chunks = content.split("\n\n")

            for chunk in chunks:
                documents.append({
                    "source": filename,
                    "content": chunk
                })

# =====================
# STORE IN VECTOR DB
# =====================
# =====================
# STORE IN VECTOR DB (SAFE VERSION)
# =====================

existing = collection.get()

if len(existing["ids"]) == 0:
    for i, doc in enumerate(documents):
        collection.add(
            ids=[str(i)],
            documents=[doc["content"]],
            metadatas=[{"source": doc["source"]}],
            embeddings=[embedding_model.encode(doc["content"]).tolist()]
        )

    print("DATA STORED IN VECTOR DB ✅")
# =====================
# CHAT LOOP
# =====================
chat_history = []
while True:
    query = input("\nAsk your question (or type exit): ")

    if query.lower() == "exit":
        break

    query_embedding = embedding_model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=5
    )
    print("\n📄 Retrieved Context:\n", results["documents"][0])

    context = "\n".join(results["documents"][0])

    prompt = f"""
You are a RAG assistant.

Rules:
1. Use ONLY the context provided.
2. Do NOT guess.
3. Do NOT add extra information.
4. Answer in 1-2 sentences.

Context:
{context}

Question:
{query}
"""

    response = ollama.chat(
        model="llama3:latest",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print("\n🤖 ANSWER:\n")
    print(response["message"]["content"])