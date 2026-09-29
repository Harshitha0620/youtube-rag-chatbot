from fastapi import FastAPI

from app.api.youtube import router as youtube_router
from app.api.chat import router as chat_router
from app.api.summary import router as summary_router


app = FastAPI(
    title="YouTube RAG Chatbot",
    version="1.0.0"
)


app.include_router(
    youtube_router,
    prefix="/youtube",
    tags=["YouTube"]
)

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)

app.include_router(
    summary_router,
    prefix="/summary",
    tags=["Summary"]
)


@app.get("/")
def root():
    return {
        "message": "YouTube RAG Chatbot API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }