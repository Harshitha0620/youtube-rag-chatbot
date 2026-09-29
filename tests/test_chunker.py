from app.ingestion.chunker import (
    create_chunks
)


def test_create_chunks():

    text = (
        "Artificial intelligence is a field "
        "of computer science. " * 100
    )

    chunks = create_chunks(
        text,
        "testvideo123"
    )

    assert len(chunks) > 0

    assert chunks[0].metadata[
        "video_id"
    ] == "testvideo123"