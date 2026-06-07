import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = open("data/sample.txt", "r", encoding="utf-8").read()
chunks = [text[i:i+50] for i in range(0, len(text), 50)]
embeddings = model.encode(chunks)

client = chromadb.Client()
collection = client.get_or_create_collection(name="rag_store")

# store data
for i, chunk in enumerate(chunks):
    collection.add(
        ids=[str(i)],
        documents=[chunk],
        embeddings=[embeddings[i].tolist()]
    )

print("DATA STORED ✅")

# -------- QUERY PART --------

query = "What is this project about?"

query_embedding = model.encode([query])

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

print("\nTOP MATCHES:")
for doc in results["documents"][0]:
    print("-", doc)
