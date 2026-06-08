print("RAG FILE WORKING")

def ask_rag(query):
    return "Test response from RAG"

if __name__ == "__main__":
    while True:
        query = input("Ask: ")
        if query.lower() == "exit":
            break
        print(ask_rag(query))