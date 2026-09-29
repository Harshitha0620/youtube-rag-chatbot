from fastapi import APIRouter, HTTPException

from app.schemas.chat_schema import ChatRequest
from app.rag.rag_service import answer_question


router = APIRouter()


@router.post("/ask")
def ask_question(request: ChatRequest):

    try:

        result = answer_question(
            video_id=request.video_id,
            question=request.question
        )

        return {
            "answer": result["answer"],
            "sources": result.get("sources", [])
        }

    except Exception as e:

        print("\n==============================")
        print("ERROR IN /chat/ask")
        print(type(e).__name__)
        print(str(e))
        print("==============================\n")

        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {str(e)}"
        )