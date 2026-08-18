from app.rag.chunking import chunk_text


def test_chunk_text_returns_multiple_chunks_with_overlap() -> None:
    text = " ".join([f"sentence {index}" for index in range(40)])
    chunks = chunk_text(text, chunk_size=10, overlap=3)
    assert len(chunks) > 1
    assert chunks[0].startswith("sentence 0")
    assert chunks[1] != chunks[0]
