from langchain_chroma import Chroma

from app.config import settings
from app.embeddings.bge_embeddings import get_embeddings


# Load embedding model
embeddings = get_embeddings()


# Create ChromaDB vector store
vectorstore = Chroma(
    collection_name="youtube_transcripts",
    embedding_function=embeddings,
    persist_directory=settings.CHROMA_PERSIST_DIR,
)


def get_vectorstore():
    """
    Return the ChromaDB vector store.
    """
    return vectorstore


def add_documents(documents, video_id: str):
    """
    Add transcript chunks to ChromaDB.
    """

    for document in documents:
        document.metadata["video_id"] = video_id

    vectorstore.add_documents(documents)


def get_retriever(video_id: str | None = None, k: int = 4):
    """
    Return a ChromaDB retriever.
    """

    if video_id:
        return vectorstore.as_retriever(
            search_kwargs={
                "k": k,
                "filter": {
                    "video_id": video_id
                }
            }
        )

    return vectorstore.as_retriever(
        search_kwargs={
            "k": k
        }
    )


def get_collection_count():
    """
    Return number of stored chunks.
    """

    return vectorstore._collection.count()