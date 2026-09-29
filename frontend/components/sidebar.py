import streamlit as st


def render_sidebar():

    st.sidebar.title(
        "YouTube RAG"
    )

    st.sidebar.markdown(
        """
        ### Features

        - YouTube transcript ingestion
        - RAG-based Q&A
        - AI video summaries
        - Source retrieval
        - Ollama LLM
        - BGE-M3 embeddings
        - ChromaDB
        - LangGraph
        """
    )

    return st.sidebar.text_input(
        "FastAPI URL",
        value="http://localhost:8000"
    )