import re


def clean_transcript(text: str) -> str:
    """
    Clean YouTube transcript text.
    """

    if not text:
        return ""

    # Convert multiple spaces/newlines into single spaces
    text = re.sub(r"\s+", " ", text)

    # Remove common transcript timestamp formats
    text = re.sub(
        r"\b\d{1,2}:\d{2}(?::\d{2})?\b",
        "",
        text
    )

    # Remove unwanted square-bracket text such as [Music]
    text = re.sub(r"\[[^\]]*\]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()