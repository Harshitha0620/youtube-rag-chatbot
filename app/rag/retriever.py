from app.vectorstore.chroma_store import get_vectorstore
from app.config import settings


def retrieve_documents(
    question: str,
    video_id: str
):

    vectorstore = get_vectorstore()

    documents = vectorstore.similarity_search(
        question,
        k=settings.RETRIEVAL_K,
        filter={
            "video_id": video_id
        }
    )

    return documents