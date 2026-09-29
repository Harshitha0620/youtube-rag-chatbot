import requests


API_URL = "http://localhost:8000"


# ---------------------------------------------------------
# INGEST VIDEO
# ---------------------------------------------------------

def ingest_video(
    youtube_url: str
):

    response = requests.post(

        f"{API_URL}/youtube/ingest",

        json={
            "url": youtube_url
        },

        timeout=300
    )

    response.raise_for_status()

    return response.json()


# ---------------------------------------------------------
# CHAT
# ---------------------------------------------------------

def chat(
    video_id: str,
    question: str
):

    response = requests.post(

        f"{API_URL}/chat/ask",

        json={

            "video_id": video_id,

            "question": question
        },

        timeout=300
    )

    response.raise_for_status()

    return response.json()


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

def summary(
    video_id: str
):

    response = requests.post(

        f"{API_URL}/summary/{video_id}",

        timeout=300
    )

    response.raise_for_status()

    return response.json()