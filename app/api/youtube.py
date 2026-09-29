from fastapi import APIRouter, HTTPException

from app.schemas.youtube_schema import YouTubeRequest

from app.ingestion.youtube_loader import (
    extract_video_id,
    extract_transcript,
    extract_video_title
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


router = APIRouter()


@router.post("/ingest")
def ingest_youtube_video(request: YouTubeRequest):

    try:

        # ==========================================
        # STEP 1: Get YouTube URL
        # ==========================================

        youtube_url = str(request.url)

        print("\n==============================")
        print("STEP 1: YouTube URL")
        print(youtube_url)


        # ==========================================
        # STEP 2: Extract Video ID
        # ==========================================

        video_id = extract_video_id(
            youtube_url
        )

        print("STEP 2: Video ID")
        print(video_id)


        # ==========================================
        # STEP 3: Extract Exact YouTube Title
        # ==========================================

        print("STEP 3: Extracting YouTube title...")

        video_title = extract_video_title(
            youtube_url
        )

        print("Video Title:")
        print(video_title)


        # ==========================================
        # STEP 4: Extract Transcript
        # ==========================================

        print("STEP 4: Extracting transcript...")

        transcript = extract_transcript(
            youtube_url
        )

        print(
            f"Transcript extracted: "
            f"{len(transcript)} characters"
        )


        # ==========================================
        # STEP 5: Clean Transcript
        # ==========================================

        print("STEP 5: Cleaning transcript...")

        cleaned_transcript = clean_transcript(
            transcript
        )

        print(
            f"Cleaned transcript: "
            f"{len(cleaned_transcript)} characters"
        )

        if not cleaned_transcript:

            raise ValueError(
                "Transcript became empty after cleaning."
            )


        # ==========================================
        # STEP 6: Create Chunks
        # ==========================================

        print("STEP 6: Creating chunks...")

        chunks = create_chunks(
            cleaned_transcript,
            video_id
        )

        print(
            f"Chunks created: {len(chunks)}"
        )

        if not chunks:

            raise ValueError(
                "No chunks were created from transcript."
            )


        # ==========================================
        # STEP 7: Store in ChromaDB
        # ==========================================

        print("STEP 7: Storing chunks in ChromaDB...")

        add_documents(
            chunks,
            video_id
        )

        print(
            "Documents stored successfully."
        )


        # ==========================================
        # STEP 8: Return Response
        # ==========================================

        print(
            "STEP 8: Video processed successfully"
        )

        print("==============================\n")


        return {
            "message": "Video processed successfully",

            "video_id": video_id,

            "title": video_title,

            "url": youtube_url,

            "chunks": len(chunks)
        }


    except Exception as e:

        print("\n==============================")
        print("ERROR IN /youtube/ingest")
        print(type(e).__name__)
        print(str(e))
        print("==============================\n")

        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {str(e)}"
        )