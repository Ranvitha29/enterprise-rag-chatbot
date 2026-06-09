import streamlit as st
import tempfile

from rag_chat import ask_rag
from pdf_loader import process_pdf

st.title("Enterprise RAG Chatbot")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:

        tmp_file.write(uploaded_file.read())

        pdf_path = tmp_file.name

    process_pdf(pdf_path)

    st.success("PDF uploaded successfully!")

question = st.text_input("Ask a question")

if question:

    with st.spinner("Searching knowledge base..."):

        answer = ask_rag(question)

    st.subheader("Answer")

    st.write(answer)