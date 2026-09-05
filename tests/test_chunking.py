from gerardo_rag.chunking import chunk_page


def test_chunking_preserves_page_and_overlap():
    text = " ".join(f"palabra{i}" for i in range(10))
    chunks = chunk_page(text, page=2, size=6, overlap=2)
    assert len(chunks) == 2
    assert chunks[0].page == 2
    assert chunks[0].text.split()[-2:] == chunks[1].text.split()[:2]
