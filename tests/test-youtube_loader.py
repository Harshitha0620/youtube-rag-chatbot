from app.ingestion.youtube_loader import (
    extract_video_id
)


def test_extract_standard_url():

    url = (
        "https://www.youtube.com/watch?v="
        "dQw4w9WgXcQ"
    )

    assert extract_video_id(
        url
    ) == "dQw4w9WgXcQ"


def test_extract_short_url():

    url = (
        "https://youtu.be/dQw4w9WgXcQ"
    )

    assert extract_video_id(
        url
    ) == "dQw4w9WgXcQ"


def test_invalid_url():

    assert extract_video_id(
        "https://google.com"
    ) is None