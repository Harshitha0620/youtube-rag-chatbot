from app.ingestion.youtube_loader import (
    extract_video_id,
    get_video_metadata,
    load_youtube_transcript
)


url = "https://youtu.be/DInMru2Eq6E"

print("\n==============================")
print("TESTING YOUTUBE")
print("==============================")

video_id = extract_video_id(url)

print("\nVideo ID:")
print(video_id)


print("\nTesting metadata...")

metadata = get_video_metadata(video_id)

print(metadata)


print("\nTesting transcript...")

transcript = load_youtube_transcript(video_id)

print(
    "Transcript items:",
    len(transcript)
)

print("\nFirst transcript item:")

if transcript:
    print(transcript[0])

print("\n==============================")
print("TEST COMPLETED")
print("==============================")