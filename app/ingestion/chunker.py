from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


def create_chunks(
    text: str,
    video_id: str | None = None
):
    """
    Split transcript into chunks.

    video_id is optional so the function can be used
    independently as well as during YouTube ingestion.
    """

    if not text or not text.strip():
        return []

    chunks = text_splitter.split_text(text)

    documents = []

    for index, chunk in enumerate(chunks):

        metadata = {
            "chunk_index": index
        }

        if video_id:
            metadata["video_id"] = video_id

        documents.append(
            Document(
                page_content=chunk,
                metadata=metadata
            )
        )

    return documents