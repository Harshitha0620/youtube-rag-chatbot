from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL


def extract_video_id(youtube_url: str) -> str:
    """
    Extract YouTube video ID from different YouTube URL formats.
    """

    parsed_url = urlparse(youtube_url)

    hostname = parsed_url.hostname

    # Standard YouTube URL
    # https://www.youtube.com/watch?v=VIDEO_ID
    if hostname in ["www.youtube.com", "youtube.com"]:

        query_params = parse_qs(parsed_url.query)

        if "v" in query_params:
            return query_params["v"][0]

        # YouTube Shorts
        # https://www.youtube.com/shorts/VIDEO_ID
        if parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/shorts/")[1].split("/")[0]

    # Short YouTube URL
    # https://youtu.be/VIDEO_ID
    if hostname in ["youtu.be", "www.youtu.be"]:

        video_id = parsed_url.path.strip("/").split("/")[0]

        if video_id:
            return video_id

    raise ValueError("Invalid YouTube URL")


def extract_transcript(youtube_url: str) -> str:
    """
    Extract transcript from YouTube video.
    """

    video_id = extract_video_id(youtube_url)

    api = YouTubeTranscriptApi()

    transcript = api.fetch(video_id)

    transcript_text = " ".join(
        item.text
        for item in transcript
    )

    if not transcript_text.strip():
        raise ValueError(
            "YouTube transcript is empty."
        )

    return transcript_text


def extract_video_title(youtube_url: str) -> str:
    """
    Extract the exact title of the YouTube video.
    """

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }

    with YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            youtube_url,
            download=False
        )

        title = info.get("title")

        if not title:
            raise ValueError(
                "Could not retrieve YouTube video title."
            )

        return title