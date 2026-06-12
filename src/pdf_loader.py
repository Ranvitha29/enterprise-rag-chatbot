def process_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    # Reset the collection by deleting and recreating it
    global collection, chroma_client

    try:
        chroma_client.delete_collection("rag_store")
    except:
        pass

    collection = chroma_client.get_or_create_collection("rag_store")

    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk)

        collection.add(
            ids=[f"pdf_{i}"],
            documents=[chunk],
            embeddings=[embedding.tolist()]
        )

    print("PDF STORED IN CHROMADB ✅")