print("RAG FILE WORKING")

from sentence_transformers import SentenceTransformer
import chromadb
import os
from groq import Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
import os

# =====================
# EMBEDDING MODEL
# =====================
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# =====================
# VECTOR DB
# =====================
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("rag_store")

# =====================
# LOAD FILES
# =====================
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
# RAG FUNCTION
# =====================
def ask_rag(query):

    query_embedding = embedding_model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=5
    )

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

       response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
# =====================
# TERMINAL CHAT
# =====================
if __name__ == "__main__":

    while True:

        query = input("\nAsk your question (or type exit): ")

        if query.lower() == "exit":
            break

        answer = ask_rag(query)

        print("\n🤖 ANSWER:\n")
        print(answer)