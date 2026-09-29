import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    # Application
    APP_NAME = os.getenv(
        "APP_NAME",
        "YouTube RAG Chatbot"
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "True"
    ).lower() == "true"

    # Ollama
    OLLAMA_BASE_URL = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    LLM_MODEL = os.getenv(
        "LLM_MODEL",
        "llama3.2"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "bge-m3"
    )

    # ChromaDB
    CHROMA_PERSIST_DIR = os.getenv(
        "CHROMA_PERSIST_DIR",
        "./data/chroma_db"
    )

    CHROMA_COLLECTION = os.getenv(
        "CHROMA_COLLECTION",
        "youtube_transcripts"
    )

    # Transcript
    TRANSCRIPT_DIR = os.getenv(
        "TRANSCRIPT_DIR",
        "./data/transcripts"
    )

    # RAG
    CHUNK_SIZE = int(
        os.getenv("CHUNK_SIZE", "800")
    )

    CHUNK_OVERLAP = int(
        os.getenv("CHUNK_OVERLAP", "120")
    )

    RETRIEVAL_K = int(
        os.getenv("RETRIEVAL_K", "5")
    )

    # MySQL
    MYSQL_HOST = os.getenv(
        "MYSQL_HOST",
        "localhost"
    )

    MYSQL_PORT = int(
        os.getenv("MYSQL_PORT", "3306")
    )

    MYSQL_DATABASE = os.getenv(
        "MYSQL_DATABASE",
        "youtube_rag"
    )

    MYSQL_USER = os.getenv(
        "MYSQL_USER",
        "root"
    )

    MYSQL_PASSWORD = os.getenv(
        "MYSQL_PASSWORD",
        ""
    )

    @property
    def DATABASE_URL(self):

        return (
            f"mysql+pymysql://"
            f"{self.MYSQL_USER}:"
            f"{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:"
            f"{self.MYSQL_PORT}/"
            f"{self.MYSQL_DATABASE}"
        )


settings = Settings()


# Compatibility aliases
# These allow older project files to continue working.

APP_NAME = settings.APP_NAME
APP_VERSION = settings.APP_VERSION
DEBUG = settings.DEBUG

OLLAMA_BASE_URL = settings.OLLAMA_BASE_URL
LLM_MODEL = settings.LLM_MODEL
EMBEDDING_MODEL = settings.EMBEDDING_MODEL

CHROMA_PERSIST_DIR = settings.CHROMA_PERSIST_DIR
CHROMA_COLLECTION = settings.CHROMA_COLLECTION

TRANSCRIPT_DIR = settings.TRANSCRIPT_DIR

CHUNK_SIZE = settings.CHUNK_SIZE
CHUNK_OVERLAP = settings.CHUNK_OVERLAP
RETRIEVAL_K = settings.RETRIEVAL_K

MYSQL_HOST = settings.MYSQL_HOST
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DATABASE = settings.MYSQL_DATABASE
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD

DATABASE_URL = settings.DATABASE_URL