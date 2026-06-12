def process_pdf(pdf_path):

    # Clear old PDF data from ChromaDB
    try:
        existing = collection.get()
        if existing["ids"]:
            collection.delete(ids=existing["ids"])
    except Exception:
        pass

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    for i, chunk in enumerate(chunks):

        embedding = model.encode(chunk)

        collection.add(
            ids=[f"pdf_{i}"],
            documents=[chunk],
            embeddings=[embedding.tolist()]
        )

    print("PDF STORED IN CHROMADB ✅")