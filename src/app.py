import streamlit as st
from rag_chat import ask_rag
st.title("Enterprise RAG Chatbot")

question = st.text_input("Ask a question")

if question:
    with st.spinner("Searching knowledge base..."):
        answer = ask_rag(question)

    st.subheader("Answer")
    st.write(answer)