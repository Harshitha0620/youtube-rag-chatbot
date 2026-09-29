from datetime import datetime

from app.database.connection import SessionLocal
from app.database.models import Video, ChatMessage, Base


def initialize_database():
    from app.database.connection import engine

    Base.metadata.create_all(bind=engine)


def init_db():
    return initialize_database()


def create_or_update_video(
    video_id: str,
    title: str,
    channel_name: str,
    video_url: str,
    transcript_available: bool = True,
    chunk_count: int = 0
):
    db = SessionLocal()

    try:
        video = (
            db.query(Video)
            .filter(Video.video_id == video_id)
            .first()
        )

        if video:
            video.title = title
            video.channel_name = channel_name
            video.video_url = video_url
            video.transcript_available = transcript_available
            video.chunk_count = chunk_count

        else:
            video = Video(
                video_id=video_id,
                title=title,
                channel_name=channel_name,
                video_url=video_url,
                transcript_available=transcript_available,
                chunk_count=chunk_count,
                created_at=datetime.utcnow()
            )

            db.add(video)

        db.commit()
        db.refresh(video)

        return video

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_video(video_id: str):
    db = SessionLocal()

    try:
        return (
            db.query(Video)
            .filter(Video.video_id == video_id)
            .first()
        )

    finally:
        db.close()


def save_chat_message(
    video_id: str,
    question: str,
    answer: str
):
    db = SessionLocal()

    try:
        message = ChatMessage(
            video_id=video_id,
            question=question,
            answer=answer,
            created_at=datetime.utcnow()
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()