from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Video(Base):
    __tablename__ = "videos"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    video_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    title = Column(
        String(500),
        nullable=True
    )

    channel_name = Column(
        String(255),
        nullable=True
    )

    video_url = Column(
        Text,
        nullable=False
    )

    transcript_available = Column(
        Boolean,
        default=True
    )

    chunk_count = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    video_id = Column(
        String(50),
        nullable=False,
        index=True
    )

    question = Column(
        Text,
        nullable=False
    )

    answer = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )