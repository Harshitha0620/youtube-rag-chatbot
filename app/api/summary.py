from fastapi import APIRouter, HTTPException

from app.rag.rag_service import answer_question


router = APIRouter()


@router.post("/{video_id}")
def generate_summary(video_id: str):

    try:

        question = """
        Provide a clear and detailed summary of this YouTube video.

        Include:
        1. Main topic
        2. Important concepts
        3. Key points
        4. Important examples or explanations
        5. Final conclusion

        Use only the information available in the video transcript.
        """

        result = answer_question(
            video_id=video_id,
            question=question
        )

        return {
            "video_id": video_id,
            "summary": result["answer"],
            "sources": result.get("sources", [])
        }

    except Exception as e:

        print("\n==============================")
        print("ERROR IN /summary")
        print(type(e).__name__)
        print(str(e))
        print("==============================\n")

        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {str(e)}"
        )