from app.rag.rag_service import (
    format_documents
)

from langchain_core.documents import (
    Document
)


def test_format_documents():

    documents = [
        Document(
            page_content="AI is useful."
        ),
        Document(
            page_content="RAG retrieves context."
        )
    ]

    result = format_documents(
        documents
    )

    assert "AI is useful." in result

    assert "RAG retrieves context." in result