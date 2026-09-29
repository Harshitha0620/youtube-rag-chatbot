# YouTube RAG Chatbot

A GenAI application that allows users to upload/process a YouTube
video and ask questions about its transcript.

The system uses:

- LLM
- RAG
- LangChain
- LangGraph
- Ollama
- Llama 3.2
- BGE-M3
- ChromaDB
- FastAPI
- Streamlit
- MySQL
- Docker

---

## Architecture

YouTube URL
     |
     v
YouTube Transcript API
     |
     v
Transcript Cleaner
     |
     v
Text Chunking
     |
     v
BGE-M3 Embeddings
     |
     v
ChromaDB
     |
     v
Retriever
     |
     v
LangGraph
     |
     +----------------+
     |                |
     v                v
   Chat             Summary
     |                |
     +--------+-------+
              |
              v
         Llama 3.2
              |
              v
         FastAPI API
              |
              v
         Streamlit UI

---

# Requirements

Python 3.10+

Ollama

MySQL

---

# Ollama Setup

Install Ollama.

Then download the models:

```bash
ollama pull llama3.2