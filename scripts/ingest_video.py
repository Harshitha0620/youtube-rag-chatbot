import sys
from pathlib import Path


ROOT_DIR = Path(
    __file__
).resolve().parent.parent

sys.path.append(
    str(ROOT_DIR)
)


from app.ingestion.youtube_loader import (
    extract_video_id,
    get_video_metadata,
    load_youtube_transcript
)

from app.ingestion.transcript_cleaner import (
    clean_transcript
)

from app.ingestion.chunker import (
    create_chunks
)

from app.vectorstore.chroma_store import (
    add_documents
)

from app.database.repository import (
    create_video,
    initialize_database
)


def ingest(
    youtube_url: str
):

    initialize_database()

    video_id = extract_video_id(
        youtube_url
    )

    if not video_id:

        raise ValueError(
            "Invalid YouTube URL"
        )

    print(
        f"Video ID: {video_id}"
    )

    print(
        "Fetching metadata..."
    )

    metadata = get_video_metadata(
        video_id
    )

    print(
        f"Title: {metadata['title']}"
    )

    print(
        "Fetching transcript..."
    )

    transcript = load_youtube_transcript(
        video_id
    )

    cleaned = clean_transcript(
        transcript["text"]
    )

    print(
        "Creating chunks..."
    )

    documents = create_chunks(
        cleaned,
        video_id
    )

    print(
        f"Created {len(documents)} chunks."
    )

    print(
        "Creating embeddings and storing in ChromaDB..."
    )

    add_documents(
        documents
    )

    create_video(
        video_id=video_id,
        url=youtube_url,
        title=metadata["title"],
        channel=metadata["channel"],
        duration=metadata["duration"]
    )

    print(
        "Video ingestion completed successfully."
    )


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "Usage:"
        )

        print(
            "python scripts/ingest_video.py "
            "<youtube_url>"
        )

        sys.exit(1)

    ingest(
        sys.argv[1]
    )