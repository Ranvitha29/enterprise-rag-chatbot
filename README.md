# Enterprise RAG Chatbot

## Overview

Enterprise RAG Chatbot is a Retrieval-Augmented Generation (RAG) application built using Python, Streamlit, ChromaDB, Sentence Transformers, and Ollama.

The chatbot retrieves relevant information from company documents and generates accurate responses based on the retrieved context.

## Features

* Document-based question answering
* ChromaDB vector database
* Sentence Transformer embeddings
* Ollama Llama 3 integration
* Streamlit web interface
* Retrieval-Augmented Generation (RAG)

## Tech Stack

* Python
* Streamlit
* ChromaDB
* Sentence Transformers
* Ollama
* Llama 3

## Project Structure

enterprise-rag/

* data/
* src/

  * app.py
  * rag_chat.py
  * pdf_loader.py
* requirements.txt

## Sample Questions

* What are the office timings?
* How many annual leave days do employees get?
* Is work from home allowed?
* How many hours should employees work per day?

## How to Run

1. Activate virtual environment
2. Install requirements
3. Start Ollama
4. Run Streamlit

```bash
streamlit run src/app.py
```

## Author

Ranvitha Nayakwadi
